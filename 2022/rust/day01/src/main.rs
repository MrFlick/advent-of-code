use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;


fn main() {
    if let Ok(lines) = read_lines("../../py/2022-Day01.txt") {
        let mut current_elf = 0;
        let mut elves : Vec<i32> = Vec::new();
        for line in lines {
            if let Ok(calories) = line {
                if calories.is_empty() {
                    elves.push(current_elf);
                    current_elf = 0;
                } else {
                    current_elf += calories.parse::<i32>().unwrap();
                }
            }
        }
        elves[0];
        elves.sort_by(|a, b| b.cmp(a));
        println!("{}", elves[0]);
        let bestthree :i32 = elves[0..3].iter().sum();
        println!("{bestthree}");
    }
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
