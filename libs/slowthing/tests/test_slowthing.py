import slowthing


def test_add_and_describe():
    assert slowthing.add_and_describe(2, 3) == "2 + 3 = 5"


def test_sum_iterable():
    assert slowthing.sum_iterable([1, 2, 3, 4, 5]) == 15
    assert slowthing.sum_iterable(range(10)) == 45
    assert slowthing.sum_iterable([]) == 0


def test_summarise():
    out = slowthing.summarise([1, 2, 3, 4, 5])
    assert out["n"] == 5
    assert out["sum"] == 15
    assert out["mean"] == 3.0
    assert out["variance"] == 2.0


def test_summarise_empty():
    out = slowthing.summarise([])
    assert out["n"] == 0
    assert out["sum"] == 0
    assert out["mean"] is None
    assert out["variance"] is None
