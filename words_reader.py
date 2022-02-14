from pathlib import Path
import json
from typing import Dict, List

_JSON_FILE = Path("./words.json")


def read_json_file(f: Path = _JSON_FILE) -> Dict[str, List[str]]:
    """Read the json file containing all words."""
    if not f.exists():
        raise Exception(f"The json file located at {f.as_posix()} cannot be found!")
    with f.open("r") as opened_f:
        return json.load(opened_f)


def write_json_file(data: Dict[str, List[str]], loc: Path = _JSON_FILE) -> None:
    """Re-write the words json file with the provided dictionary."""
    with loc.open("w") as f:
        json.dump(data, f, indent=4)
