
fn main(){ 
 } 

/*
 xs are coefficients of a polynomial.
    find_zero find x such that poly(x) = 0.
    find_zero returns only only zero point, even if there are many.
    Moreover, find_zero only takes list xs having even number of coefficients
    and largest non zero coefficient as it guarantees
    a solution.
    
*/

use std::{slice::Iter, cmp::{max, self}, mem::replace, collections::{HashSet, HashMap}, ops::Index, ascii::AsciiExt};
use rand::Rng;
use regex::Regex;
use md5;
use std::any::{Any, TypeId};

fn poly(xs: &Vec<f64>, x: f64) -> f64 {


        let mut sum = 0.0;
        for i in 0..xs.len() {
            sum += xs[i] * x.powi(i as i32);
        }
        sum
    }
    
    fn find_zero(xs: &Vec<f64>) -> f64 {
        let mut ans = 0.0;
        let mut value = poly(xs, ans);
        while value.abs() > 1e-6 {
            let mut driv = 0.0;
            for i in 1..xs.len() {
                driv += xs[i] * ans.powi((i - 1) as i32) * (i as f64);
            }
            ans = ans - value / driv;
            value = poly(xs, ans);
        }
        ans
    }

/*
#[cfg(test)]
mod tests {
    use super::*;

#[test]
    fn test_poly() {
        let mut rng = rand::thread_rng();
        let mut solution: f64;
        let mut ncoeff: i32;
        for _ in 0..100 {
            ncoeff = 2 * (1 + rng.gen_range(0, 4));
            let mut coeffs = vec![];
            for _ in 0..ncoeff {
                let coeff = -10 + rng.gen_range(0, 21);
                if coeff == 0 {
                    coeffs.push(1.0);
                } else {
                    coeffs.push(coeff as f64);
                }
            }
            solution = find_zero(&coeffs);
            assert!(poly(&coeffs, solution).abs() < 1e-3);
        }
    }

}
*/