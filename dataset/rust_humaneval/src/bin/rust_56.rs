
fn main(){ 
 } 

/*
 brackets is a string of "<" and ">".
    return True if every opening bracket has a corresponding closing bracket.
    
*/

use std::{slice::Iter, cmp::{max, self}, mem::replace, collections::{HashSet, HashMap}, ops::Index, ascii::AsciiExt};
use rand::Rng;
use regex::Regex;
use md5;
use std::any::{Any, TypeId};

fn correct_bracketing(bkts:&str) -> bool{


    let mut level:i32=0;

    for i in 0..bkts.len(){

        if bkts.chars().nth(i).unwrap()== '<' {level+=1;}
        
        if bkts.chars().nth(i).unwrap() == '>' {  level-=1;}
      
        if level<0 {return false;} 
    }
    if level!=0 {return false;}
    return true;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_correct_bracketing() {
        assert!(correct_bracketing("<>"));
        assert!(correct_bracketing("<<><>>"));
        assert!(correct_bracketing("<><><<><>><>"));
        assert!(correct_bracketing("<><><<<><><>><>><<><><<>>>"));
        assert!(!(correct_bracketing("<<<><>>>>")));
        assert!(!(correct_bracketing("><<>")));
        assert!(!(correct_bracketing("<")));
        assert!(!(correct_bracketing("<<<<")));
        assert!(!(correct_bracketing(">")));
        assert!(!(correct_bracketing("<<>")));
        assert!(!(correct_bracketing("<><><<><>><>><<>")));
        assert!(!(correct_bracketing("<><><<><>><>>><>")));
    }

}