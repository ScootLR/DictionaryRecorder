from pathlib import Path
from typing import List
import json
from typing import Dict, Tuple

JSON_FILE = Path("./words.json")
NEW_JSON_FILE = Path("./new_words.json")


def read_json_file(f: Path = JSON_FILE) -> List[str]:
    with f.open("r") as opened_f:
        return json.load(opened_f)


def write_json_file(results: Dict[str, List[Tuple[str, str, str]]], loc: Path = NEW_JSON_FILE) -> None:
    with loc.open("w") as f:
        json.dump(results, f, indent=4)


LETTERS = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z")


def remove_duplicates(results) -> Dict[str, List[str]]:
    new_results = {x: [] for x in LETTERS}
    for key in LETTERS:
        words = results[key]

        prev_word = ""
        for word_and_defn in words:
            word = word_and_defn[0]
            if word != prev_word:
                new_results[key].append(word)
                prev_word = word

    return new_results

if __name__ == "__main__":
    result = read_json_file()
    new_results = remove_duplicates(result)
    write_json_file(new_results)
    print("No")
