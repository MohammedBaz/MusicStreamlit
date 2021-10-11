import streamlit as st
import pretty_midi
import numpy as np 
import pandas
import os
import base64
from typing import List

st.title("AIMC")
st.header("Artificial Intelligence Music Composer")

uploaded_file = st.file_uploader("upload", type=['wav','mp3','mid'], accept_multiple_files=False, key=123456)
if uploaded_file is not None:
  if uploaded_file.name.endswith('wav'):
    audio = uploaded_file.read()
    fileType=('wav')
    st.audio(audio, format='audio/wav')
  elif uploaded_file.name.endswith('mp3'):
    audio = uploaded_file.read()
    fileType=('mp3')
    st.audio(audio, format='audio/mp3')
  elif uploaded_file.name.endswith('mid'):
    audio = pretty_midi.PrettyMIDI(uploaded_file)
    fileType=('mid')
    st.write("replay of mid is not supported currently")
    

