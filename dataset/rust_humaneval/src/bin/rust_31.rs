
fn main(){ 
 } 

/*
Return true if a given number is prime, and false otherwise.
    
*/

use std::{slice::Iter, cmp::{max, self}, mem::replace, collections::{HashSet, HashMap}, ops::Index, ascii::AsciiExt};
use rand::Rng;
use regex::Regex;
use md5;
use std::any::{Any, TypeId};

fn is_prime(n:i32) -> bool{


    if n < 2{
    return false;
}
for k in 2..n-1 {
    if n % k == 0{
        return false;
    }
}
return true;

}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_is_prime() {
        assert!(is_prime(6) == false);
        assert!(is_prime(101) == true);
        assert!(is_prime(11) == true);
        assert!(is_prime(13441) == true);
        assert!(is_prime(61) == true);
        assert!(is_prime(4) == false);
        assert!(is_prime(1) == false);
        assert!(is_prime(5) == true);
        assert!(is_prime(11) == true);
        assert!(is_prime(17) == true);
        assert!(is_prime(5 * 17) == false);
        assert!(is_prime(11 * 7) == false);
        assert!(is_prime(13441 * 19) == false);
    }

}