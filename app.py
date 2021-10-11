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

  # This funciton is defined to store the file uploded by the user into temporary file.
  # This is required as some librarys and functions requies to pass the file location instead of its contents, 
  # However,  file_uploader reads the file as a file-like Byte IO type : more can be found on 
  # https://blog.jcharistech.com/2021/01/21/how-to-save-uploaded-files-to-directory-in-streamlit-apps/
  # As I prefer to work on Streamlit share, I have no prioir informaion about the file location, 
  # so I use os.getcwd() to get the working directory and then add the uploaded file into it. 
  # we then use open-write to crate the file, more on https://www.w3schools.com/python/python_file_write.asp
  # finally we return the file locaion so that it can be used by other funciton 
  with open(os.path.join(os.getcwd(),uploaded_file.name),"wb") as f:
      f.write(uploaded_file.getbuffer())
  return (os.path.join(os.getcwd(),uploaded_file.name))

def PlayBackMusicFile(FileLocation FileType):
  # This function generate audio widget, replay the contents found in FileLocation
  # full specficaion for this widget can be found https://docs.streamlit.io/en/stable/api.html
  # This function requires file locaton and its type
  # I tried to find a way to run mid but failed.any help is appricated 
  audio_file = open(FileLocation, 'rb')
  audio_bytes = audio_file.read()
  st.audio(audio_bytes, format='audio/'+FileType)

uploaded_file = st.file_uploader("upload", type=['wav','mp3','mid'], accept_multiple_files=False, key=123456) # Create new file uploader instance and let it accept audio files
if uploaded_file is not None:                               # Just to check that the user has its own input to the filed_uploader
  if not (uploaded_file.name.endswith('mid')):              # if the file is not mid, i.e., it is .wav or.mp3 then
    FileLocation=StoretheUpoldedFile(uploaded_file)         # Store the file and get its location information 
    PlayBackMusicFile(FileLocation,FileLocation.split(".")[-1]) # pass the locaiona and extension to PlayBackMusicFile to replay its contents
    
