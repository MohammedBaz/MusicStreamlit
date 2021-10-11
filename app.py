import streamlit as st
import pretty_midi
import numpy as np 
import pandas
import os
import base64
from typing import List


def UploadedFileHandler(uploaded_file):
  if uploaded_file is not None:
    if uploaded_file.name.endswith('wav'):
      audio = uploaded_file.read()
      fileType=('wav')
    elif uploaded_file.name.endswith('mp3'):
      audio = uploaded_file.read()
      fileType=('mp3')
    else:
      audio = pretty_midi.PrettyMIDI(uploaded_file)
      fileType=('mid')         
   return (audio,fileType)

st.title("AIMC")
st.header("Artificial Intelligence Music Composer")
from BackEndPrediction import Prediction
uploaded_file = st.file_uploader("upload", type=['wav','mp3','mid'], accept_multiple_files=False, key=123456)
UploadedFileHandler(uploaded_file)
st.write("FileUploaded",UploadedFileHandler(uploaded_file)[1])


    
  #  st.audio(audio, format='audio/wav')

