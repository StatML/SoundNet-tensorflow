import numpy as np
import librosa
import pdb

local_config = {
            'batch_size': 64, 
            'load_size': 22050*20,
            }


def load_from_list(name_list, config=local_config):
    audios = np.zeros([config['batch_size'], config['load_size'], 1, 1])
    for idx, audio_path in enumerate(name_list):
        # By default, librosa will resample the signal to 22050Hz. And range in (-1., 1.)
        sound_sample, _ = load_audio(audio_path)
        audios[idx] = preprocess(sound_sample, config)
        
    return audios


def load_from_txt(txt_name, config=local_config):
    with open(txt_name, 'r') as handle:
        txt_list = handle.read().splitlines()

    audios = []
    for idx, audio_path in enumerate(txt_list):
        # By default, librosa will resample the signal to 22050Hz. And range in (-1., 1.)
        sound_sample, _ = load_audio(audio_path)
        audios.append(preprocess(sound_sample, config))
        
    return audios


# NOTE: Load an audio as the same format in soundnet
# 1. Keep original sample rate (which conflicts their own paper)
# 2. Use first channel in multiple channels
# 3. Keep range in [-256, 256]

def load_audio(audio_path, sr=None):
    sound_sample, sr = librosa.load(audio_path, sr=sr, mono=False)

    return sound_sample, sr


def preprocess(raw_audio, config=local_config):
    # Select first channel (mono)
    if len(raw_audio.shape) > 1:
        raw_audio = raw_audio[0]

    # Make range [-256, 256]
    raw_audio *= 256.0

    # Use length or Not
    length = config['load_size']
    if length is not None:
        raw_audio = raw_audio[:length]

    # Check conditions
    assert len(raw_audio.shape) == 1, "It seems this audio contains two channels, we only need the first channel"
    assert np.max(raw_audio) <= 256, "It seems this audio contains signal that exceeds 256"
    assert np.min(raw_audio) >= -256, "It seems this audio contains signal that exceeds -256"

    # Shape to 1 x DIM x 1 x 1
    raw_audio = np.reshape(raw_audio, [1, -1, 1, 1])

    return raw_audio.copy()


