import pandas as pd
import numpy as np
import os
from pathlib import Path
from cust_enum import SLICE_SET_TYPE


class Decorator:
    @staticmethod
    def app_path(fn_path_str):
        """Decorating function to help check and build path

        Arguments:
            fn_path_str {str} -- function which returns path string

        Returns:
            function -- checking path name function
        """
        def create_path(*original_args):
            Path(fn_path_str(*original_args)).mkdir(parents=True, exist_ok=True)
            return fn_path_str(*original_args)
        return create_path

    @staticmethod
    def app_file(fn_file_str):
        """Decorating function to help check existing of the file

        Arguments:
            fn_file_str {str} -- function which returns file string

        Returns:
            function -- checking file name function
        """
        def check_file(*original_args):
            if not os.path.exists(*original_args):
                print(f'{original_args[0]} is not found')
                exit()
            return fn_file_str(*original_args)
        return check_file


class Helper:
    """The class contains static methods for general utilizations.
    """

    class File_manipulation:
        @staticmethod
        def load_data_csv(filename, date_format, index_col):
            """Load csv

            Arguments:
                filename {str} -- csv name
                date_format {str} -- date format e.g. '%Y-%m-%d %H:%M:%S' or '%d-%m-%y %H:%M'
                index_col {int} -- column no. of index

            Returns:
                DataFrame -- read data
            """
            def dateparse(x): return pd.datetime.strptime(x, date_format)

            return pd.read_csv(filename, index_col=index_col, parse_dates=True,
                               date_parser=dateparse, dtype=object).sort_index()

        @staticmethod
        def save_array(filename, content):
            """save array to file .npy

            Arguments:
                filename {str} -- file name
                content {ndarray} -- array
            """
            np.save(filename, content)

        @staticmethod
        def load_array(filename):
            """load array from file .npy

            Arguments:
                filename {str} -- file name

            Returns:
                ndarray -- array
            """
            return np.load(filename)

        @staticmethod
        def check_array_files(filenames):
            """check existing of files

            Arguments:
                filenames {array} -- array of filenames

            Returns:
                bool -- True: exist, False: not exist
            """
            for filename in filenames:
                if not os.path.exists(filename):
                    return False
            return True

        @staticmethod
        @Decorator.app_path
        def data_path(path_name):
            """Return checked path name

            Arguments:
                path_name {str} -- assigned path name

            Returns:
                str -- existing path name
            """
            return path_name

        @staticmethod
        @Decorator.app_file
        def data_file(file_name):
            """Return checked file name

            Arguments:
                file_name {str} -- assigned file name

            Returns:
                str -- existing file name
            """
            return file_name


class Slice_set:
    def __init__(self, slice_set_type, start=None, len=None, end=None):
        """This object automatically calculate parameters to slice data for state used in environment. This object makes sure the valid start and end, and would print len except data_set_type is all. start, len and end arguments can be None only one or less except data_set_type is all.

        Arguments:
            slice_set_type {SLICE_SET_TYPE} -- selected slice set as options in SLICE_SET_TYPE

        Keyword Arguments:
            start {int} -- positive for START_LEFT, negative for START_RIGHT (default: {None})
            len {int} -- sliced data length (default: {None})
            end {int} -- positive for START_LEFT, negative for START_RIGHT (default: {None})
        """
        self.slice_set_type = slice_set_type
        self.start = start
        self.len = len
        self.end = end
        if self.slice_set_type is SLICE_SET_TYPE.ALL:
            self.param_all()
        else:
            self.param_partial()

    def param_all(self):
        self.start = 0
        self.end = None

    def param_partial(self):
        if self.end is None and self.len is not None:
            self.end = self.start + self.slice_set_type.value*(self.len)
            if self.end == 0:
                self.end = None
        elif self.start is None:
            self.start = self.end-self.slice_set_type.value*(self.len)
        elif self.len is None:
            self.len = self.slice_set_type.value*(self.end - self.start)
        self.start *= self.slice_set_type.value
        if self.end is not None:
            self.end *= self.slice_set_type.value
