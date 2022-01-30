import sounddevice as sd
import pydub
from pathlib import Path
import numpy as np


SAMPLING_FREQUENCY = 44100
RECORD_DURATION = 3  # seconds


def record_audio(out_file: Path,
                 sampling_frequency: int = SAMPLING_FREQUENCY,
                 record_duration: int = RECORD_DURATION
                 ) -> None:
    """
    Record audio over the default audio input device and save it to a file.

    Parameters
    ----------
    out_file : Path
        The location to save the audio file to.
        The suffix of this must be .mp3
    sampling_frequency : int, optional
        The sampling frequency at which to record the audio
    record_duration : int
        The number of seconds to record for
    """
    assert out_file.suffix == ".mp3", f"The output file's suffix is not .mp3, it is: {out_file.suffix}"
    assert not out_file.exists(), "The output file already exists!"

    samples = record_duration * sampling_frequency
    recording = sd.rec(samples, samplerate=sampling_frequency, channels=2)
    print("Recording...")
    sd.wait()
    print("Finished recording")

    print(f"Saving audio to {out_file.as_posix()}")
    channels = 2
    # Un-normalise
    unnormalised_audio = np.int16(recording * 2 ** 15)
    song = pydub.AudioSegment(unnormalised_audio.tobytes(),
                              frame_rate=sampling_frequency,
                              sample_width=2,
                              channels=channels)
    song.export(out_file, format="mp3", bitrate="320k")
