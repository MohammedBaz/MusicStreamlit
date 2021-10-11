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
  
    

