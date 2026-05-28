import geoanalysis


def test_tile_stats_basic():
    points = [(0.5, 0.5), (1.0, 1.0), (5.0, 5.0), (10.0, 10.0)]
    out = geoanalysis.tile_stats(
        points=points,
        tile_min=(0.0, 0.0),
        tile_max=(2.0, 2.0),
        reference=(0.0, 0.0),
    )
    assert out["inside"] == 2
    assert out["nearest"] == (0.5, 0.5)
    assert out["mean_distance"] is not None
    assert out["mean_distance"] > 0


def test_tile_stats_empty():
    out = geoanalysis.tile_stats(
        points=[(5.0, 5.0)],
        tile_min=(0.0, 0.0),
        tile_max=(1.0, 1.0),
        reference=(0.0, 0.0),
    )
    assert out == {"inside": 0, "mean_distance": None, "nearest": None}
