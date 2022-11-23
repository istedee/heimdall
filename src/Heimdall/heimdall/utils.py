"""Utility methods for Heimdall"""

from pathlib import Path


def return_path(relpath: str) -> str:
    """Path helper, to give full path.
    Helps to call the function or package
    from anywhere."""
    return Path(__file__).parent / relpath
