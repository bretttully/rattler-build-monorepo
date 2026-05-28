//! Tile/bbox operations built on `geocompute-core`.

use geocompute_core::{Point, distance};

pub fn point_in_tile(p: Point, tile_min: Point, tile_max: Point) -> bool {
    p.x >= tile_min.x && p.x <= tile_max.x && p.y >= tile_min.y && p.y <= tile_max.y
}

pub fn nearest_point(target: Point, candidates: &[Point]) -> Option<Point> {
    candidates.iter().copied().min_by(|a, b| {
        distance(target, *a)
            .partial_cmp(&distance(target, *b))
            .expect("non-NaN distances")
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn containment() {
        let p = Point::new(1.0, 1.0);
        assert!(point_in_tile(p, Point::new(0.0, 0.0), Point::new(2.0, 2.0)));
        assert!(!point_in_tile(p, Point::new(2.0, 2.0), Point::new(3.0, 3.0)));
    }

    #[test]
    fn nearest() {
        let target = Point::new(0.0, 0.0);
        let candidates = [Point::new(5.0, 5.0), Point::new(1.0, 1.0), Point::new(10.0, 10.0)];
        assert_eq!(nearest_point(target, &candidates), Some(Point::new(1.0, 1.0)));
        assert_eq!(nearest_point(target, &[]), None);
    }
}
