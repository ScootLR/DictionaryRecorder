from source.keyboard_listener import Listener
from source.audio_recorder import Recorder
from pathlib import Path




def main() -> None:
    """The main function."""


    recorder = Recorder()
    listener = Listener(recorder)
    listener.start()
    listener.join()


if __name__ == "__main__":
    main()
