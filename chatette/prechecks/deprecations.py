from .pyversion import _is_deprecated_python_version, _get_python_version_as_str
from chatette.utils import print_warn


def check_for_deprecations():
    _check_python_version()

def _check_python_version():
    if _is_deprecated_python_version():
        print_warn(
            "Python v" + _get_python_version_as_str() + \
            " will not be supported in the future. " + \
            "Please upgrade Python whenever possible."
        )
