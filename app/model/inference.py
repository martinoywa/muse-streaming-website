from pathlib import Path

import torch

from .loaders import *
from .preprocessor import *

audio_weights = Path("app/model/weights/audio/base.v2.36perB")
lyrics_weights = Path("app/model/weights/lyrics/model_bert.bin")

audio_model = load_audio_model(audio_weights)
lyrics_model = load_lyrics_model(lyrics_weights)


def audio_inference(spectrogram):
    input = audio_preprocessor(spectrogram)
    output = audio_model(input)
    
    return output


def lyrics_inference(lyrics):
    input = lyrics_preprocessor(lyrics)
    output = lyrics_model(**input)

    return output


def aggregate_inference(spectrogram, lyrics):
    audio_output = audio_inference(spectrogram)
    lyrics_output = lyrics_inference(lyrics)
    aggregate = audio_output + lyrics_output[0]
    _, pred = torch.max(aggregate, dim=1)
    pred = pred.item() + 1

    return pred
