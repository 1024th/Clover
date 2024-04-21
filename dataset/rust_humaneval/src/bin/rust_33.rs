
fn main(){ 
 } 

/*
This function takes a list l and returns a list l' such that
    l' is identical to l in the indicies that are not divisible by three, while its values at the indicies that are divisible by three are equal
    to the values of the corresponding indicies of l, but sorted.
    
*/

use std::{slice::Iter, cmp::{max, self}, mem::replace, collections::{HashSet, HashMap}, ops::Index, ascii::AsciiExt};
use rand::Rng;
use regex::Regex;
use md5;
use std::any::{Any, TypeId};

fn sort_third(l: Vec<i32>) -> Vec<i32> {


    let mut third = vec![];
    let mut out:Vec<i32> = vec![];

    for (indx,elem) in l.iter().enumerate(){
        if indx%3 == 0 && indx != 0{
            third.push(elem)
        }
    }
    third.sort();
    let mut indx_t:usize = 0;

    for i in 0..l.len() {
        if i%3 == 0 && i != 0{
            if indx_t < third.len(){
                out.push(*third[indx_t]);
                indx_t += 1;
        }
        }else{
            out.push(l[i]);
        }
        
    }
    return out;
}

#[cfg(test)]
mod tests {
    use super::*;

 #[test]
    fn test_sort_third() {
        let mut l = vec![1, 2, 3];
        assert_eq!(sort_third(l), vec![1, 2, 3]);
        l = vec![5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10];
        assert_eq!(sort_third(l), vec![5, 3, -5, 1, -3, 3, 2, 0, 123, 9, -10]);
        l = vec![5, 8, -12, 4, 23, 2, 3, 11, 12, -10];
        assert_eq!(sort_third(l), vec![5, 8, -12, -10, 23, 2, 3, 11, 12, 4]);
        l = vec![5, 6, 3, 4, 8, 9, 2];
        assert_eq!(sort_third(l), vec![5, 6, 3, 2, 8, 9, 4]);
        l = vec![5, 8, 3, 4, 6, 9, 2];
        assert_eq!(sort_third(l), vec![5, 8, 3, 2, 6, 9, 4]);
        l = vec![5, 6, 9, 4, 8, 3, 2];
        assert_eq!(sort_third(l), vec![5, 6, 9, 2, 8, 3, 4]);
        l = vec![5, 6, 3, 4, 8, 9, 2, 1];
        assert_eq!(sort_third(l), vec![5, 6, 3, 2, 8, 9, 4, 1]);
    }

}