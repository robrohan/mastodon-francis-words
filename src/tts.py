# https://colab.research.google.com/drive/1bzNckroXrwgPMdBdnipcnQcryM4Wnf_4?authuser=1#scrollTo=XcJM7cXPglxJ
import sys
sys.path.append("TensorFlowTTS/")

import tensorflow as tf
import numpy as np
from scipy.io import wavfile
from tensorflow_tts.inference import TFAutoModel
from tensorflow_tts.inference import AutoProcessor
from pydub.silence import split_on_silence
from pydub import AudioSegment

##############################################################################

end_marker = ". : : ::...................;;;;;;;;;;-----------;;;;;;;;;;;;;;;;;;;;; A"

tacotron2 = None
mb_melgan = None
processor = None

def download_models():
  global tacotron2
  global mb_melgan 
  global processor
  
  tacotron2 = TFAutoModel.from_pretrained("tensorspeech/tts-tacotron2-synpaflex-fr", name="tacotron2")
  mb_melgan = TFAutoModel.from_pretrained("tensorspeech/tts-mb_melgan-synpaflex-fr", name="mb_melgan")
  processor = AutoProcessor.from_pretrained("tensorspeech/tts-tacotron2-synpaflex-fr")

    #tacotron2 = TFAutoModel.from_pretrained("tensorspeech/tts-tacotron2-ljspeech-en", name="tacotron2")
  #mb_melgan = TFAutoModel.from_pretrained("tensorspeech/tts-melgan-ljspeech-en", name="mb_melgan")
  #processor = AutoProcessor.from_pretrained("tensorspeech/tts-tacotron2-ljspeech-en")
  
  # setup window for tacotron2 if you want to try
  tacotron2.setup_window(win_front=5, win_back=5)

##############################################################################

def do_synthesis(input_text, text2mel_model, vocoder_model, text2mel_name, vocoder_name):
  input_ids = processor.text_to_sequence(input_text)

  # text2mel part
  if text2mel_name == "TACOTRON":
    x, mel_outputs, stop_token_prediction, alignment_history = text2mel_model.inference(
        tf.expand_dims(tf.convert_to_tensor(input_ids, dtype=tf.int32), 0),
        tf.convert_to_tensor([len(input_ids)], tf.int32),
        tf.convert_to_tensor([0], dtype=tf.int32)
    )
    print(stop_token_prediction.shape[1])
  else:
    raise ValueError("Only TACOTRON is supported on text2mel_name")

  # vocoder part
  if vocoder_name == "MB-MELGAN":
    # tacotron-2 generate noise in the end symtematic, let remove it :v.
    # if text2mel_name == "TACOTRON":
    #   remove_end = 1024
    # else:
    #   remove_end = 1
    # audio = vocoder_model.inference(mel_outputs)[0, :-remove_end, 0]
    audio = vocoder_model.inference(mel_outputs)[0, :-1, 0]
  else:
    raise ValueError("Only MB_MELGAN are supported on vocoder_name")

  if text2mel_name == "TACOTRON":
    return mel_outputs.numpy(), alignment_history.numpy(), audio.numpy()
  else:
    return mel_outputs.numpy(), audio.numpy()

def text2wav(text, filepath):
  download_models()
  text = text + end_marker
  _, _, audios = do_synthesis(text, tacotron2, mb_melgan, "TACOTRON", "MB-MELGAN")

  scaled = np.int16(audios / np.max(np.abs(audios)) * 32767)

  aud = AudioSegment(scaled.tobytes(),
                    frame_rate = 24000,
                    sample_width = scaled.dtype.itemsize, # audios.dtype.itemsize,
                    channels = 1)
  aud = aud.set_frame_rate(24000)

  # use split on silence method to split the audio based on the silence, 
  # here we can pass the min_silence_len as silent length threshold 
  # in ms and intensity threshold
  audio_chunks = split_on_silence(
      aud,
      min_silence_len = 600,
      silence_thresh = -35,
      keep_silence = 200)

  audio_processed = sum(audio_chunks[0:1])
  audio_processed = np.array(audio_processed.get_array_of_samples())

  # wavfile.write(filepath, 24000, audios)
  wavfile.write(filepath, 24000, audio_processed)

# input_text = "qui est-ce? Je cherche le métro et l’aéroport."
# text2wav(input_text, "demo.wav")
