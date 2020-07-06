import tables


class H5FileHelper(object):

    def __init__(self, filename):
        self.filename = filename

    @property
    def recordings(self):
        h5file = tables.open_file(self.filename, mode="r")
        recording_names = list(h5file.root._v_children.keys())

        recording_names = [x for x in recording_names if not "label" in x and
                           not "annotation" in x]
        recording_names.sort()
        h5file.close()

        return recording_names

    @property
    def annotations(self):
        h5file = tables.open_file(self.filename, mode="r")
        recording_annotations = list(h5file.root._v_children.keys())

        recording_annotations = [x for x in recording_annotations
                                 if "annotation" in x]
        recording_annotations.sort()
        h5file.close()

        return recording_annotations

    def is_annotated(self, recording_name):
        return True in [recording_name in x for x in self.annotations]