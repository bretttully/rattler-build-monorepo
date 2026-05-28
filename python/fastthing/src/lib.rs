//! PyO3 bindings re-exporting both fastthing-core and fastthing-stats.

use pyo3::prelude::*;

#[pyfunction]
fn add(a: i64, b: i64) -> i64 {
    fastthing_core::add(a, b)
}

#[pyfunction]
fn sum_list(xs: Vec<i64>) -> i64 {
    fastthing_core::sum_slice(&xs)
}

#[pyfunction]
fn mean(xs: Vec<i64>) -> Option<f64> {
    fastthing_stats::mean(&xs)
}

#[pyfunction]
fn variance(xs: Vec<i64>) -> Option<f64> {
    fastthing_stats::variance(&xs)
}

#[pymodule]
fn fastthing(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(add, m)?)?;
    m.add_function(wrap_pyfunction!(sum_list, m)?)?;
    m.add_function(wrap_pyfunction!(mean, m)?)?;
    m.add_function(wrap_pyfunction!(variance, m)?)?;
    Ok(())
}
