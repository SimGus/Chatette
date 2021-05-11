from sys import version_info


def _get_python_version_as_str():
    return str(version_info[0]) + '.' + str(version_info[1])


def _is_supported_python_version():
    return version_info[0] == 3 \
        or version_info[0] == 2 and version_info[1] == 7

def _is_deprecated_python_version():
    return version_info[0] == 2 \
        or version_info[0] == 3 and version_info[1] < 3
