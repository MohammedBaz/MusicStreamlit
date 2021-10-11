import streamlit as st
import pretty_midi
import numpy as np 
import pandas
import os
import base64
from typing import List
import wave

st.title("AIMC")
st.header("Artificial Intelligence Music Composer")
import os
st.write(os.getcwd())
with open('myfile.txt', 'w') as fp:
    pass
print


def GetParametersofWav(wavfile):
  wav_file=wave.open(wavfile, "rb")
  n_channels = wav_file.getnchannels()      # Number of channels. (1=Mono, 2=Stereo).
  sample_width = wav_file.getsampwidth()    # Sample width in bytes.
  framerate = wav_file.getframerate()       # Frame rate.
  n_frames = wav_file.getnframes()          # Number of frames.
  comp_type = wav_file.getcomptype()        # Compression type (only supports "NONE").
  comp_name = wav_file.getcompname()        # Compression name.
  st.write(n_channels)
  st.write(sample_width)
  st.write(framerate)
  st.write(n_frames)
  st.write(comp_type)
  st.write(comp_name)


def StoretheUpoldedFile(Filename):
   with open(os.path.join(os.getcwd(),uploaded_file.name),"wb") as f:
      f.write(uploaded_file.getbuffer())
  return (os.path.join(os.getcwd(),uploaded_file.name))

def PlayBackMusicFile(FileLocation FileType):
  audio_file = open(FileLocation, 'rb')
  audio_bytes = audio_file.read()
  st.audio(audio_bytes, format='audio/'+FileType)

uploaded_file = st.file_uploader("upload", type=['wav','mp3','mid'], accept_multiple_files=False, key=123456) #Create new file uploader instance and let it accept audio files
if uploaded_file is not None:                     # Just to check that the user has its own input to the filed_uploader
  if not (uploaded_file.name.endswith('wav')):
    FileLocation=StoretheUpoldedFile(uploaded_file)
    PlayBackMusicFile(FileLocation,FileLocation.split(".")[-1])
  
    

