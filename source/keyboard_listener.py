from pynput import keyboard
from .audio_recorder import Recorder
from typing import Optional
from .words_reader import WordHandler, _AUDIO_FOLDER
from pathlib import Path
import os


_LETTERS = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
            "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z")


def clear_terminal():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


class Listener(keyboard.Listener):
    """
    A class for recording audio whilst a key is held down.

    The key that needs to be held down is set to ctrl.
    """
    def __init__(self, recorder: Recorder):
        super().__init__(on_press=self.on_press, on_release=self.on_release)
        self.recorder: Recorder = recorder
        self._letter_selected: Optional[str] = None
        self._word_handler: Optional[WordHandler] = None
        self._next_word: Optional[str] = None

        clear_terminal()
        print("Select Letter")

    def on_press(self, key):
        if self._letter_selected is None:
            self._select_letter(key)
        else:
            return self._listen(key)

    def on_release(self, key):
        if isinstance(key, keyboard.Key):  # special key event
            if "ctrl" in key.name:
                assert self._next_word is not None
                f = Path(_AUDIO_FOLDER / self._letter_selected / (self._next_word + ".mp3"))
                self.recorder.stop(f)

                clear_terminal()

                self._next_word = self._word_handler.get_next_word()
                if self._next_word is None:
                    print(f"All words for letter {self._letter_selected} completed!")
                    return False

                print(f"Next word: {self._next_word}")
                print("Press the escape key to quit recording")
                print("Hold ctrl to record")

    def _select_letter(self, key):
        if key.char.capitalize() in _LETTERS:
            self._letter_selected = key.char.capitalize()
            self._word_handler = WordHandler(self._letter_selected)
            self._next_word = self._word_handler.get_next_word()
            print(f"Letter selected: {key.char.capitalize()}")
            print(f"Next word: {self._next_word}")
            print("Press the escape key to quit recording")
            print("Hold ctrl to record")
        else:
            print(f"Invalid letter: {key.char}")

    def _listen(self, key):
        if key is None:  # unknown event
            pass
        elif isinstance(key, keyboard.Key):  # special key event
            if "ctrl" in key.name:
                self.recorder.start()
            elif "esc" in key.name:
                print("Ending session")
                return False
        return True
