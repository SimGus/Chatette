from .pyversion import _is_supported_python_version, _get_python_version_as_str


class PreconditionsUnmet(Exception):
    pass


def ensure_preconditions():
    _ensure_python_version_is_supported()

def _ensure_python_version_is_supported():
    if not _is_supported_python_version():
        print(
            "[ERROR] Python v" + _get_python_version_as_str() + \
            " is not supported by Chatette. " + \
            "Please use a version of Python older than v2.7.\n"
        )
        raise PreconditionsUnmet()
