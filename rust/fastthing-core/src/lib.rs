//! Pure-Rust core of the `fastthing` package.
//!
//! Lives in the Rust-only workspace; no PyO3 dependency. The `fastthing`
//! PyO3 cdylib in `python/fastthing/` wraps these functions for Python.

pub fn add(a: i64, b: i64) -> i64 {
    a + b
}

pub fn sum_slice(xs: &[i64]) -> i64 {
    xs.iter().sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn add_works() {
        assert_eq!(add(2, 3), 5);
        assert_eq!(add(-1, 1), 0);
    }

    #[test]
    fn sum_slice_works() {
        assert_eq!(sum_slice(&[]), 0);
        assert_eq!(sum_slice(&[1, 2, 3, 4, 5]), 15);
    }
}
