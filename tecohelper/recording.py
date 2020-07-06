import numpy as np
import pandas as pd

from tecohelper.config import HIP_SENSOR, LEFT_SENSOR, \
    RIGHT_SENSOR, LEFT_SENSOR_OLD, HIP_SENSOR_OLD, RTLS_SENSOR, RIGHT_OLD_MACS


class Recording(object):

    def __init__(self, filename, recording_key):
        self._recording_key = recording_key
        self._filename = filename
        self._df = pd.read_hdf(filename, key="/{}".format(recording_key))
        self._tokens = None
        self._annotations = None
        self._start_and_stop_frames = None
        self._sensors = None

    @property
    def tokens(self):
        if self._tokens is None:
            try:
                self._tokens = pd.read_hdf(self._filename,
                                           key="/{}_labels".format(
                                               self._recording_key
                                           ))
            except KeyError:
                self._tokens = None
        return self._tokens

    @property
    def annotations(self):
        if self._annotations is None:
            try:
                self._annotations = pd.read_hdf(self._filename,
                                                key="/{}_annotations".format(
                                                    self._recording_key
                                                ))
            except KeyError:
                self._annotations = None
        return self._annotations

    @property
    def right_imu_sensor(self):
        if RIGHT_SENSOR in self.sensors:
            return RIGHT_SENSOR
        else:
            for snsr in self.sensors:
                if snsr in RIGHT_OLD_MACS:
                    return snsr

    @property
    def left_imu_sensor(self):
        if RIGHT_SENSOR in self.sensors:
            return LEFT_SENSOR
        else:
            return LEFT_SENSOR_OLD

    @property
    def hip_imu_sensor(self):
        if RIGHT_SENSOR in self.sensors:
            return HIP_SENSOR
        else:
            return HIP_SENSOR_OLD

    @property
    def right_imu_dataframe(self):
        return self._df[self._df["update_type"] == self.right_imu_sensor]

    @property
    def left_imu_dataframe(self):
        return self._df[self._df["update_type"] == self.left_imu_sensor]

    @property
    def hip_imu_dataframe(self):
        return self._df[self._df["update_type"] == self.hip_imu_sensor]

    @property
    def sensors(self):
        grpby = self._df.groupby("update_type")
        return [x for x in list(grpby.groups.keys())
                if not "RTLS" in x or x == RTLS_SENSOR]#if x in
                #[LEFT_SENSOR, LEFT_SENSOR_OLD, RIGHT_SENSOR, RIGHT_SENSOR_OLD,
                #HIP_SENSOR, HIP_SENSOR_OLD, RTLS_SENSOR]]

    @staticmethod
    def find_closest_index(df, column, value):
        exactmatch = df[df[column] == value]

        if not exactmatch.empty:
            return exactmatch.index
        else:
            lowerneighbour_ind = df[df[column] < value][column]
            if lowerneighbour_ind.shape[0] > 0:
                lowerneighbour_ind = lowerneighbour_ind.idxmax()
            else:
                lowerneighbour_ind = df.index[0]

            upperneighbour_ind = df[df[column] > value][column]
            if upperneighbour_ind.shape[0] > 0:
                upperneighbour_ind = upperneighbour_ind.idxmin()
            else:
                upperneighbour_ind = df.index[-1]

            lv = (np.max(df.at[lowerneighbour_ind, column]) if
                  type(df.at[lowerneighbour_ind, column]) == np.ndarray else
                  df.at[lowerneighbour_ind, column])
            hv = (np.min(df.at[upperneighbour_ind, column]) if
                  type(df.at[upperneighbour_ind, column]) == np.ndarray else
                  df.at[upperneighbour_ind, column])
            lower_val = value - lv
            higher_val = hv - value

            if higher_val > lower_val:
                return lowerneighbour_ind
            else:
                return upperneighbour_ind

    def get_sensor_slice_df(self, sensor_name, first_timestamp, last_timestamp):
        start_sensor = Recording.find_closest_index(
            self._df[self._df["update_type"] == sensor_name],
            "received_timestamp",
            first_timestamp
        )
        end_sensor = Recording.find_closest_index(
            self._df[self._df["update_type"] == sensor_name],
            "received_timestamp",
            last_timestamp
        )

        if isinstance(start_sensor, pd.DatetimeIndex):
            start_sensor = start_sensor.values.astype(np.int64)
            start_sensor = pd.Timestamp(start_sensor[0], unit='ns')

        if isinstance(end_sensor, pd.DatetimeIndex):
            end_sensor = end_sensor.values.astype(np.int64)
            end_sensor = pd.Timestamp(end_sensor[0], unit='ns')

        return self._df[self._df["update_type"] == sensor_name].loc[
               start_sensor:end_sensor]

    def _get_sensor_token_df(self, sensor_name, token):
        start_timestamp = self.annotations[
            self.annotations["label"] == "init.start_recording"].iloc[0][
            "start {}".format(sensor_name)]
        end_timestamp = self.annotations[
            self.annotations["label"] == "init.end_recording"].iloc[0][
            "end {}".format(sensor_name)]

        return self._df[self._df["update_type"] == sensor_name].loc[
               start_timestamp:end_timestamp]

    def _get_sensor_token_df_no_stamps(self, sensor_name, token):
        start_left = self.annotations[
            self.annotations["label"] == "init.start_recording"].iloc[0][
            "start {}".format(self.left_imu_sensor)]
        end_left = self.annotations[
            self.annotations["label"] == "init.end_recording"].iloc[0][
            "end {}".format(self.left_imu_sensor)]

        start_sensor = Recording.find_closest_index(
            self._df[self._df["update_type"] == sensor_name],
            "received_timestamp",
            start_left
        )
        end_sensor = Recording.find_closest_index(
            self._df[self._df["update_type"] == sensor_name],
            "received_timestamp",
            end_left
        )

        return self._df[self._df["update_type"] == sensor_name].loc[
               start_sensor:end_sensor]

    def get_start_timestamp(self, sensor_name):
        if "start {}".format(sensor_name) in self.annotations.keys():
            return self.annotations[
                self.annotations["label"] == "init.start_recording"].iloc[0][
                "start {}".format(sensor_name)]
        else:
            start_left = self.annotations[
                self.annotations["label"] == "init.start_recording"].iloc[0][
                "start {}".format(self.left_imu_sensor)]
            return Recording.find_closest_index(
                self._df[self._df["update_type"] == sensor_name],
                "received_timestamp",
                start_left
            )

    def get_end_timestamp(self, sensor_name):
        if "start {}".format(sensor_name) in self.annotations.keys():
            return self.annotations[
                self.annotations["label"] == "init.end_recording"].iloc[0][
                "start {}".format(sensor_name)]
        else:
            start_left = self.annotations[
                self.annotations["label"] == "init.end_recording"].iloc[0][
                "start {}".format(self.left_imu_sensor)]
            return Recording.find_closest_index(
                self._df[self._df["update_type"] == sensor_name],
                "received_timestamp",
                start_left
            )
