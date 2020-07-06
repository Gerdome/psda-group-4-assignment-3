from typing import Optional, Dict, List, Tuple

import numpy as np
import pandas as pd

from tecohelper.config import LABELS, RTLS
from tecohelper.recording import Recording


class AnvilHelper(object):

    def __init__(self, h5file, recording_key, anvil_export):
        self.recording = Recording(h5file, recording_key)
        self.anvil_annotations = pd.read_csv(anvil_export, sep=';')
        self._tokens = None
        self._end_annotation = None
        self._start_annotation = None

    def _get_token_rows(self, label_field):
        """
        Returns a dataframe to where each row contains start and end frame for
        an occurrence of the given label inside the recording.
        """
        self.anvil_annotations['block'] = (
                self.anvil_annotations[label_field].shift(1) !=
                self.anvil_annotations[label_field]).astype(int).cumsum()
        current_tokens = (
            self.anvil_annotations.reset_index().groupby(
                ['block', label_field])['index'].apply(np.array).reset_index())
        current_tokens = current_tokens[current_tokens[label_field] > 0]
        # current_tokens = current_tokens[current_tokens[label_field] == 0]
        current_tokens.drop(['block', label_field], axis=1, inplace=True)
        return current_tokens

    @property
    def start_annotation(self) -> int:
        if self._start_annotation is None:
            cf = "init.start_recording"
            rws = self._get_token_rows(cf)
            self._start_annotation = rws.iloc[0][0][
                int(len(rws.iloc[0][0]) / 2)]
        return self._start_annotation

    @property
    def end_annotation(self) -> int:
        if self._end_annotation is None:
            cf = "init.end_recording"
            rws = self._get_token_rows(cf)
            self._end_annotation = rws.iloc[0][0][int(len(rws.iloc[0][0]) / 2)]
        return self._end_annotation

    @property
    def frames_in_recording(self) -> int:
        return self.end_annotation - self.start_annotation

    @property
    def tokens(self) -> Dict[str, List[Tuple[Tuple[int, int], int]]]:
        """
        A dictionary containing a list of frame borders for all occurrences of
        a label inside a recording.
        """
        if self._tokens is None:
            rws = {}
            for lbl in LABELS:  # type: str
                brdrs = []
                cf = self._get_token_rows(lbl)
                for _, row in cf.iterrows():
                    start_frame = row[0][0]  # type: int
                    end_frame = row[0][-1]  # type: int
                    token_subtype = self.anvil_annotations[lbl][
                        row[0][0]]  # type: int
                    brdrs.append(((start_frame, end_frame), token_subtype))
                rws[lbl] = brdrs
            self._tokens = rws
        return self._tokens

    def convert_frame_borders_to_timestamps(self, sensor_name: str,
                                            frame_start: int, frame_end: int):
        """
        Converts video frame borders to timestamps for a given sensor, usable
        as an index in the recording.
        """
        if "start {}".format(sensor_name) in self.recording.annotations.keys():
            sensor_start_timestamp = self.recording.get_start_timestamp(sensor_name)
            sensor_end_timestamp = self.recording.get_end_timestamp(sensor_name)
            framedelta = (sensor_end_timestamp - sensor_start_timestamp) / self.frames_in_recording
            return (sensor_start_timestamp + (frame_start - self.start_annotation) * framedelta,
                    sensor_start_timestamp + (frame_end - self.start_annotation) * framedelta)
        else:
            return self.convert_frame_borders_to_timestamps(self.recording.left_imu_sensor,
                                                            frame_start, frame_end)

    def get_token_dataframe_for_sensor(self, sensor_name: str,
                                       frame_start: int,
                                       frame_end: int) -> pd.DataFrame:
        """
        Returns a DataFrame with sensor data of a single sensor for a specified
        slice of the recording, given by video frame borders.
        """
        timestamp_start, timestamp_end = self.convert_frame_borders_to_timestamps(
            sensor_name, frame_start, frame_end)
        df = self.recording.get_sensor_slice_df(sensor_name, timestamp_start,
                                                timestamp_end)
        return df

    def get_token_dataframe(self, label: str, token_index: int) -> Optional[
        pd.DataFrame]:
        """
        Returns a DataFrame with sensor data for a selected token from the
        recording.

        :param label: The label of the token to extract data for
        :type label: str
        :param token_index: Repetition index of the token (so n-1 for the nth
            occurrence inside the data)
        :type token_index: int
        :returns: A DataFrame with sensor data during the duration of the token
            for all sensors

            The sensor data will be reindexed and resampled to an approximate
            sample rate of 50Hz.
        :rtype: pd.DataFrame
        """
        if self.tokens is None:
            return None

        label_tokens = self.tokens[label]
        if token_index >= len(label_tokens):
            print(f"Only {len(label_tokens)} tokens available "
                  f"for label {label}!")
            return None

        (frame_start, frame_end), token_subtype = label_tokens[token_index]
        sensor_dfs = {}
        for sensor in self.recording.sensors:
            # get data frame for single sensor
            sensor_df = self.get_token_dataframe_for_sensor(sensor,
                                                            frame_start,
                                                            frame_end)
            # drop unused columns from frame
            cols_to_keep = ['device_address', 'device_timestamp',
                            'packet_number',
                            'update_type']
            cols_to_drop = []

            if sensor == self.recording.left_imu_sensor:
                cols_to_keep.append('received_timestamp')
                colpref = "left"
            elif sensor == self.recording.right_imu_sensor:
                colpref = "right"
            elif sensor == self.recording.hip_imu_sensor:
                colpref = "hip"
            else:
                if True in [RTLS in x for x in sensor_df.columns]:
                    colpref = RTLS
                else:
                    colpref = "rtls"

            for col in sensor_df.columns:
                if not (colpref in col or col in cols_to_keep):
                    cols_to_drop.append(col)

            sensor_df = sensor_df.drop(columns=cols_to_drop, axis=1)

            # rename id of rtls to rtls
            if True in [RTLS in x for x in sensor_df.columns]:
                sensor_df.rename(columns={
                    '70b3d587900101ad_accuracy': 'rtls_accuracy',
                    '70b3d587900101ad_accuracy_radius': 'rtls_accuracy_radius',
                    '70b3d587900101ad_mapped_position': 'rtls_mapped_position',
                    '70b3d587900101ad_state': 'rtls_state',
                    '70b3d587900101ad_x_filtered': 'rtls_x_filtered',
                    '70b3d587900101ad_x_unfiltered': 'rtls_x_unfiltered',
                    '70b3d587900101ad_y_filtered': 'rtls_y_filtered',
                    '70b3d587900101ad_y_unfiltered': 'rtls_y_unfiltered',
                    '70b3d587900101ad_z_filtered': 'rtls_z_filtered',
                    '70b3d587900101ad_z_unfiltered': 'rtls_z_unfiltered',
                }, inplace=True)
            sensor_dfs[sensor] = sensor_df

        # concatenate dfs and reindex to LEFT
        concatenation = [sensor_dfs[self.recording.left_imu_sensor].reset_index(drop=True), ]
        concat_names = [self.recording.left_imu_sensor]
        for sensor in self.recording.sensors:
            if sensor == self.recording.left_imu_sensor:
                continue

            if "start {}".format(sensor) in self.recording.annotations.keys():
                # left and right might differ in index
                concatenation.append(sensor_dfs[sensor].reset_index(drop=True))
                concat_names.append(sensor)
                continue

            # drop duplicated index entries (only applicable for RTLS)
            sensor_dfs[sensor] = sensor_dfs[sensor].loc[
                ~sensor_dfs[sensor].index.duplicated(keep='first')]
            # reindex to LEFT
            sensor_dfs[sensor] = sensor_dfs[sensor].reindex(
                sensor_dfs[self.recording.left_imu_sensor].index,
                method="nearest")

            concatenation.append(sensor_dfs[sensor].reset_index(drop=True))
            concat_names.append(sensor)

        # actual concatenation on column axis
        concatenated = pd.concat(concatenation, axis=1).dropna()
        #concatenated.set_index(old_index[:concatenated.shape[0]])

        sampling_rate = 50  # Hz
        frame_delay = str(int(1000 / sampling_rate)) + 'ms'
        concatenated = concatenated.set_index("received_timestamp")
        concatenated = concatenated.resample(frame_delay).mean().ffill()

        return concatenated
