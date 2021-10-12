import streamlit as st
import pretty_midi
import numpy as np 
import pandas
import os
import base64
from typing import List
import wave

st.markdown(""" <style> #MainMenu {visibility: hidden;} footer {visibility: hidden;} </style> """, unsafe_allow_html=True)
st.title("Interactive Music Composition Artifical Intelligence")
st.header("                                                   ")
MainPageDescription = st.empty()
MainPageDescription.write("""This is a beta version for an ambitious project aiming to promote the interactivity of 
         generate some musical pieces using Artificial Intelligence (AI) algorithms.
         Several AI models have been built and trained to match the variety of musical inputs ; furthermore, 
         the interface has been optimised to allow a user to add personal toutches and then to download the cratfed musical peices. 
         Wish this can aid the users to recogenise the potential rules that AI can play in art making. Source code is at:
         https://github.com/MohammedBaz/MusicStreamlit/blob/main/BackEndPrediction.py  
         """)



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

def PlayBackMusicFile(FileLocation,FileType):
  # This function generate audio widget, replay the contents found in FileLocation
  # full specficaion for this widget can be found https://docs.streamlit.io/en/stable/api.html
  # This function requires file locaton and its type
  # I tried to find a way to run mid but failed.any help is appricated 
  audio_file = open(FileLocation, 'rb')
  audio_bytes = audio_file.read()
  st.audio(audio_bytes, format='audio/'+FileType)

def get_binary_file_downloader_html(bin_file, file_label='File'):
  with open(bin_file, 'rb') as f:
    data = f.read()
  bin_str = base64.b64encode(data).decode()
  href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
  return (href)
  
#uploaded_file = st.file_uploader("Uplod AudioFile Here or leave it blank for random starting", type=['wav','mp3','mid'], accept_multiple_files=False, key=123456) 
# Create new file uploader instance and let it accept audio files
#add_selectbox = st.sidebar.selectbox("How to prefer to strat with",("Load some audio files", "Use some random Notes", "Use pretrainned Audios"))

with st.sidebar.expander("How to prefer to strat with:"):
  add_selectbox=st.radio("you can upload your audio samples or use ours:", ("Upload some audio files", "Use some random Notes", "Use pretrainned Audios"),index=1)
if(add_selectbox=="Upload some audio files"):
  MainPageDescription .empty()       
  uploaded_file = MainPageDescription.file_uploader("Uplod AudioFile Here or leave it blank if other options are selected",
                                     type=['wav','mp3','mid'], accept_multiple_files=False, key=123456) 
  if uploaded_file is not None:                               # Just to check that the user has its own input to the filed_uploader
    if not (uploaded_file.name.endswith('mid')):              # if the file is not mid, i.e., it is .wav or.mp3 then
        FileLocation=StoretheUpoldedFile(uploaded_file)         # Store the file and get its location information 
        FileType=FileLocation.split(".")[-1]
    PlayBackMusicFile(FileLocation,FileLocation.split(".")[-1]) # pass the locaiona and extension to PlayBackMusicFile to replay its contents
with st.sidebar.expander("Add your personal touch, if wish:"):
  PredictionHorizontal = st.number_input("Select the Prediction Horizonal, in seconds",min_value=60, max_value =300,value=120,step=10)
  st.slider("Select the Inputshape, in sec",0,300,120) #here should be changed in accordnace with the inputs 
with st.sidebar.expander("Takeout your art piece"):
  st.write("Notthing tillnow")
  #st.download_button(label="DOWNLOAD!",data="trees",file_name=FileLocation,mime='audio/.'+FileType)
with st.sidebar.container():
  st.write("About")
  st.write("This is a simple apps demoenstrates for the user how advanved artifical intellgience techniques can be readily adopted")



#st.markdown(get_binary_file_downloader_html('newMid.mid', 'Audio'), unsafe_allow_html=True)

