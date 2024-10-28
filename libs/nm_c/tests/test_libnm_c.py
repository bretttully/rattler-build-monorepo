import numpy as np
from nm_c import libnm_c


def test_doc():
    assert libnm_c.__doc__ != ""


def test_fast_sum():
    a = np.array([1, 2, 3])
    assert libnm_c.fast_sum(a) == a.sum()
