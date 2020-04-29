from pathlib import Path


class Decorator:
    @staticmethod
    def app_path(fn_path_str):
        """Decorating function to help check and build path

        Arguments:
            fn_path_str {str} -- function which returns path string

        Returns:
            string -- path string
        """
        def create_path(*original_args):
            Path(fn_path_str(*original_args)).mkdir(parents=True, exist_ok=True)
            return fn_path_str(*original_args)
        return create_path


class Helper:
    class File_manipulation:
        @staticmethod
        @Decorator.app_path
        def data_path(path_name):
            return path_name


class Path_info:

    version = 0

    data_path = Helper.File_manipulation.data_path(f'./data/')
    data_csv_path = Helper.File_manipulation.data_path(f'{data_path}csv/')
    data_csv_path = Helper.File_manipulation.data_path(f'{data_path}arr/')

    model_path = Helper.File_manipulation.data_path(f'./model/')


def test():
    members = [attr for attr in dir(Path_info) if not callable(
        getattr(Path_info, attr)) and not attr.startswith("__")]
    print(members)


test()
