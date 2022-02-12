from pathlib import Path
from typing import List
import json

JSON_FILE = Path("./words.json")


# def read_sql_file() -> str:
#     """
#     Returns the dictionary in one long string.
#     """
#     all_text = SQL_FILE.read_text()
#     reduced_text = all_text.split(' VALUES ', maxsplit=1)[1]
#     reduced_text = reduced_text[::-1].split("00004!*/", maxsplit=1)[1][::-1][:-1]
#
#     return reduced_text


# def separate_words(string_repr: str) -> List[str]:
#     """
#
#     """
#     separated_words = []
#     index = 0
#     while string_repr:
#         if index > 2 and string_repr[index - 3: index] == "),(":
#             part = string_repr[:index - 2]
#             if len(part) == 1:
#                 raise Exception("Failure again")
#             separated_words.append(part)
#             string_repr = string_repr[index - 1:]
#             index = 0
#             print(part)
#         elif index >= len(string_repr):
#             part = string_repr[:-1]
#             separated_words.append(part)
#             break
#         else:
#             index += 1
#
#     return separated_words
#
#
# def get_dictionary() -> List[str]:
#     """
#
#     """
#     unseparated_dictionary = read_sql_file()
#     separated_parts = separate_words(unseparated_dictionary)
#     return separated_parts


def read_json_file(f: Path = JSON_FILE) -> List[str]:
    with f.open("r") as opened_f:
        return json.load(opened_f)


# def write_json_file(results: Dict[str, List[Tuple[str, str, str]]], loc: Path = JSON_FILE_3) -> None:
#     with loc.open("w") as f:
#         json.dump(results, f, indent=4)


# def split_results(results):
#     new_results = {}
#     for res in results:
#         first_letter = res[0][0].capitalize()
#         if first_letter not in new_results:
#             new_results[first_letter] = []
#         new_results[first_letter].append(res)
#
#     for letter in new_results:
#         new_results[letter] = sorted(new_results[letter], key=lambda x: x[0].capitalize())
#
#     sorted_keys = sorted(new_results.keys())
#     sorted_dict = {}
#     for key in sorted_keys:
#         sorted_dict[key] = new_results[key]
#     return sorted_dict


if __name__ == "__main__":
    result = read_json_file()
    print("No")
