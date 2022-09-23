from os import listdir


def is_namedtuple_instance(obj):
    """Check if the object is an instance of a named tuple.

    SRC: http://stackoverflow.com/a/2166841/4549891

    :param obj: an object to test
    :type  obj: any
    :return: True or False
    :rtype: bool
    """
    object_type = type(obj)
    bases = object_type.__bases__
    if len(bases) != 1 or bases[0] != tuple:
        return False
    fields = getattr(object_type, '_fields', None)
    if not isinstance(fields, tuple):
        return False
    return all(type(n) == str for n in fields)


def path_to_local_file(relative_path):
    """ files required for tests should be stored in /features/files,
    utility function to give you a relative path to there

    :param relative_path: relative path within /features/files
    :type  relative_path: str
    :return: full relative path within the test directory
    :rtype:  str
    """
    return f'./features/files/{relative_path}'


def list_local_dir(directory_name):
    """" List the contents of a directory in /features/files

    :param directory_name: name of directory as in /features/files
    :type  directory_name: str
    :return: list of files in directory
    :rtype:  list
    """
    dir_path = path_to_local_file(directory_name)
    return listdir(dir_path)
