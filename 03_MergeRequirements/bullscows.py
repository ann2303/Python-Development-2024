import argparse
from typing import Tuple, List
import random
from urllib import request
from cowsay import get_random_cow, cowsay

def bullscows(guess: str, secret: str) -> Tuple[int, int]:
    letters = set(secret)
    bulls = 0
    cows = 0
    for i in range(len(secret)):
        if guess[i] == secret[i]:
            bulls += 1
        elif guess[i] in letters:
            cows += 1
    return bulls, cows

def inform(format_string: str, bulls: int, cows: int) -> None:
    cowfile = get_random_cow()
    print(cowsay(format_string.format(bulls, cows), cow=cowfile))

    
def ask(prompt: str, valid: List[str] = None) -> str:
    cowfile = get_random_cow()
    print(cowsay(prompt, cow=cowfile))
    word = input()
    if valid:
        while word not in valid:
            print("Слово не допустимо!")
            print(cowsay(prompt, cow=cowfile))
            word = input()
    return word


def gameplay(ask: callable, inform: callable, words: List[str]) -> int:
    secret = random.choice(words)
    secret_len = len(secret)
    bulls, cows = 0, 0
    attempts = 0
    while bulls < secret_len:
        guess = ask("Введите слово: ", words)
        bulls, cows = bullscows(guess, secret)
        inform("Быки: {}, Коровы: {}", bulls, cows)
        attempts += 1
        
    return attempts

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Игра \"Быки и коровы\"")
    parser.add_argument("words", help="Словарь возможных слов для догадок")
    parser.add_argument("wlen", type=int, default=5, nargs='?', help="Длина секретного слова и слова-догадки")
    args = parser.parse_args()
    
    try:
        request.urlretrieve(args.words, "words_file")
        wfile = "words_file"
    except:
        wfile = args.words
    
    with open(wfile, "r") as f:
        words = [i[:-1] for i in f.readlines() if len(i) == args.wlen + 1]
        
    print(f"Всего попыток: {gameplay(ask, inform, words)}")
    