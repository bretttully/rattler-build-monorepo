//! PyO3 bindings re-exporting geocompute-core + geocompute-tiles.

use geocompute_core::Point;
use pyo3::prelude::*;

#[pyfunction]
fn distance(a: (f64, f64), b: (f64, f64)) -> f64 {
    geocompute_core::distance(Point::new(a.0, a.1), Point::new(b.0, b.1))
}

#[pyfunction]
fn point_in_tile(p: (f64, f64), tile_min: (f64, f64), tile_max: (f64, f64)) -> bool {
    geocompute_tiles::point_in_tile(
        Point::new(p.0, p.1),
        Point::new(tile_min.0, tile_min.1),
        Point::new(tile_max.0, tile_max.1),
    )
}

#[pyfunction]
fn nearest_point(target: (f64, f64), candidates: Vec<(f64, f64)>) -> Option<(f64, f64)> {
    let cands: Vec<Point> = candidates.into_iter().map(|(x, y)| Point::new(x, y)).collect();
    geocompute_tiles::nearest_point(Point::new(target.0, target.1), &cands).map(|p| (p.x, p.y))
}

#[pymodule]
fn geocompute(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(distance, m)?)?;
    m.add_function(wrap_pyfunction!(point_in_tile, m)?)?;
    m.add_function(wrap_pyfunction!(nearest_point, m)?)?;
    Ok(())
}
