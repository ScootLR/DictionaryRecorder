from pathlib import Path
import json
from typing import Dict, List, Optional

_JSON_FILE = Path("./words.json")
_AUDIO_FOLDER = Path("./audio")


class WordHandler:
    def __init__(self, letter: str):
        self._letter: str = letter
        self._words: List[str] = read_json_file().get(self._letter, [])
        self._word_index: int = -1
        self._letter_folder: Path = Path(_AUDIO_FOLDER / self._letter)

        self._setup()

    def _setup(self):
        if not _AUDIO_FOLDER.exists():
            _AUDIO_FOLDER.mkdir()
        if not self._letter_folder.exists():
            self._letter_folder.mkdir()

    def get_next_word(self) -> Optional[str]:
        """
        Fetch the next word to record.

        Returns None if all words recorded.
        """
        self._word_index += 1
        while self._word_index < len(self._words):
            word = self._words[self._word_index]
            f = Path(self._letter_folder / (word + ".mp3"))
            if not f.exists():
                return word
            else:
                self._word_index += 1
        return None


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
