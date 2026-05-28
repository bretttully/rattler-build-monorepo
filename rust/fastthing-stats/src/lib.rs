//! Statistics on slices of integers. Built on `fastthing-core`.

pub fn mean(xs: &[i64]) -> Option<f64> {
    if xs.is_empty() {
        return None;
    }
    let s = fastthing_core::sum_slice(xs);
    Some(s as f64 / xs.len() as f64)
}

pub fn variance(xs: &[i64]) -> Option<f64> {
    let m = mean(xs)?;
    let sq_diff_sum: f64 = xs.iter().map(|&x| (x as f64 - m).powi(2)).sum();
    Some(sq_diff_sum / xs.len() as f64)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn empty() {
        assert_eq!(mean(&[]), None);
        assert_eq!(variance(&[]), None);
    }

    #[test]
    fn small() {
        assert_eq!(mean(&[1, 2, 3, 4, 5]), Some(3.0));
        assert!((variance(&[2, 4, 4, 4, 5, 5, 7, 9]).unwrap() - 4.0).abs() < 1e-9);
    }
}
