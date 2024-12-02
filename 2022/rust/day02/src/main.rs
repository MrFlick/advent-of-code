use std::fs::File;
use std::io::{self, BufRead};
use std::collections::HashMap;
use std::path::Path;

#[derive(PartialEq, Eq, Hash)]
enum GameResult {
    Lose=0,
    Draw,
    Win    
}

impl From<usize> for GameResult {
    fn from(orig: usize) -> Self {
        match orig {
            0 => GameResult::Lose,
            1 => GameResult::Draw,
            2 => GameResult::Win,
            _ => GameResult::Draw
        }
    }
}


fn main() {
    let game_result: [[GameResult; 3] ; 3] = [
        [GameResult::Draw, GameResult::Win, GameResult::Lose],
        [GameResult::Lose, GameResult::Draw, GameResult::Win],
        [GameResult::Win, GameResult::Lose, GameResult::Draw]
    ];

    let play_result: [[u32; 3] ; 3] = [
        [2, 0, 1],
        [0, 1, 2],
        [1, 2, 0]
    ];

    let decode_actions: HashMap<char, usize> = HashMap::from([
        ('X', 0), ('Y', 1), ('Z', 2),
        ('A', 0), ('B', 1), ('C', 2)
    ]);

    let result_points: HashMap<GameResult, u32> = HashMap::from([
        (GameResult::Win, 6),
        (GameResult::Draw, 3),
        (GameResult::Lose, 0)
    ]);

    let mut score1:u32 = 0;
    let mut score2:u32 = 0;
    if let Ok(lines) = read_lines("../../py/2022-Day02.txt") {
        for line in lines {
            if let Ok(play) = line {
                let actions: Vec<usize> = play.split(' ')
                    .map(|c| c.chars().next().expect("empty"))
                    .map(|c| decode_actions[&c])
                    .collect();
                score1 = score1 + result_points[&game_result[actions[0]][actions[1]]] + (actions[1] as u32)+ 1;
                score2 = score2 + result_points[&GameResult::from(actions[1])] + play_result[actions[0]][actions[1]] + 1;
            } else {
                println!("Cannot read value");
            }
        }
    } else {
        println!("File Error");
    }
    println!("Score 1 {score1}");
    println!("Score 2 {score2}");
}


fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
