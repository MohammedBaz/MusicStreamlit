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
  WaveFile=wave.open(wavfile, "rb")
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



uploaded_file = st.file_uploader("upload", type=['wav','mp3','mid'], accept_multiple_files=False, key=123456)
if uploaded_file is not None:
  if uploaded_file.name.endswith('wav'):
    audio = uploaded_file.read()
    fileType=('wav')
    st.audio(audio, format='audio/wav')
    with open(os.path.join(os.getcwd(),uploaded_file.name),"wb") as f:
         f.write(uploaded_file.getbuffer())
    GetParametersofWav(os.path.join(os.getcwd(),uploaded_file.name)         
   # from pydub import AudioSegment
   # file_var = AudioSegment.from_ogg(uploaded_file)
   # file_var.export('filename.wav', format='wav')
   # GetParametersofWav(file_var)
  elif uploaded_file.name.endswith('mp3'):
    audio = uploaded_file.read()
    fileType=('mp3')
    st.audio(audio, format='audio/mp3')
    with open(os.path.join(os.getcwd(),uploaded_file.name),"wb") as f:
         f.write(uploaded_file.getbuffer())
  elif uploaded_file.name.endswith('mid'):
    audio = pretty_midi.PrettyMIDI(uploaded_file)
    fileType=('mid')
    st.write("replay of mid is not supported currently")
 
  
    

