from nm_a import __version__
from nm_a.some_func import func_a


def test_version():
    assert __version__ >= "0.0.0"


def test_func_a():
    assert func_a() is None
