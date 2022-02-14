from pynput import keyboard
import numpy as np
from pathlib import Path
import sounddevice as sd
import pydub
import time
from typing import Optional


class Recorder:
    """
    A class for recording audio and saving to a file.

    Will start recording when the start() method is called, and stop when the stop() method is called.

    Parameters
    ----------
    filename : Path
        The location to save the audio to
        Should be a .mp3 file
    sampling_frequency : int, optional
        The sampling frequency to use
        Defaults to 44100 Hz
    channels : int, optional
        The number of channels to sample over
        Defaults to 2
    initial_buffer_size_seconds : int, optional
        The maximum amount of time you will be recording for
        This should be longer than the duration you intend to record for
        Defaults to 60 seconds
    """
    def __init__(self,
                 filename: Path,
                 sampling_frequency: int = 44100,
                 channels: int = 2,
                 initial_buffer_size_seconds: int = 60):
        self._filename: Path = filename
        self._sampling_frequency: int = sampling_frequency
        self._channels: int = channels
        self._initial_buffer_size_seconds: int = initial_buffer_size_seconds
        self._recording: bool = False
        self._buffer = np.zeros((self._initial_buffer_size_seconds * self._sampling_frequency, self._channels),
                                dtype=np.float32)
        self._recording_start_time: Optional[float] = None
        self._recording_end_time: Optional[float] = None

        assert self._filename.suffix == ".mp3", f"The output file's suffix is not .mp3, it is: {self._filename.suffix}"
        if self._filename.exists():
            self._filename.unlink()

    def start(self) -> None:
        """Start recording audio."""
        if not self._recording:
            self._recording_start_time = time.time()
            sd.rec(out=self._buffer, samplerate=self._sampling_frequency, channels=self._channels)
            print('Recording')
            self._recording = True

    def stop(self) -> None:
        """Stop recording audio and save to disk."""
        if self._recording:
            self._recording_end_time = time.time()
            sd.stop()

            self._recording = False
            print('Finished recording')

            self._save_audio_to_file()

    def _save_audio_to_file(self) -> None:
        assert isinstance(self._recording_start_time, float), "The recording start time was not saved"
        assert isinstance(self._recording_end_time, float), "The recording end time was not saved"
        assert self._recording_end_time > self._recording_start_time, "The end of the recording was before the start!"
        assert self._recording_end_time < self._recording_start_time + self._initial_buffer_size_seconds, \
            "The audio recording was too long for the buffer"

        print(f"Saving to file {self._filename.as_posix()}")

        length_of_recording = self._recording_end_time - self._recording_start_time  # seconds
        samples_to_keep = int(np.ceil(length_of_recording * self._sampling_frequency))

        unnormalised_audio = np.int16(self._buffer[:samples_to_keep] * 2 ** 15)
        song = pydub.AudioSegment(unnormalised_audio.tobytes(),
                                  frame_rate=self._sampling_frequency,
                                  sample_width=2,
                                  channels=self._channels)

        song.export(self._filename, format="mp3", bitrate="320k")


class Listener(keyboard.Listener):
    """
    A class for recording audio whilst a key is held down.

    The key that needs to be held down is set to ctrl.
    """
    def __init__(self, recorder: Recorder):
        super().__init__(on_press=self.on_press, on_release=self.on_release)
        self.recorder: Recorder = recorder

    def on_press(self, key):
        if key is None:  # unknown event
            pass
        elif isinstance(key, keyboard.Key):  # special key event
            if key.ctrl:
                self.recorder.start()

    def on_release(self, key):
        if isinstance(key, keyboard.Key):  # special key event
            if key.ctrl:
                self.recorder.stop()
                return False


if __name__ == "__main__":
    f = Path("./test.mp3")
    recorder = Recorder(f)
    listener = Listener(recorder)
    listener.start()
    listener.join()
