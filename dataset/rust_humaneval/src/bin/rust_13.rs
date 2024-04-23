fn main() {}

/*
 Return a greatest common divisor of two integers a and b

*/

fn greatest_common_divisor(mut a: i32, mut b: i32) -> i32 {
    while b > 0 {
        (a, b) = (b, a % b);
    }
    return a;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_greatest_common_divisor() {
        assert!(greatest_common_divisor(3, 7) == 1);
        assert!(greatest_common_divisor(10, 15) == 5);
        assert!(greatest_common_divisor(49, 14) == 7);
        assert!(greatest_common_divisor(144, 60) == 12);
    }
}
