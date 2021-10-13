import streamlit as st
import pretty_midi
import numpy
import pandas
import base64
from typing import List
import wave
from InputHandlingandDisplay import StoretheUpoldedFile
from MidiFeatures import GeneratemidFile
import io
from scipy.io import wavfile
import os
import music21
################reconsidering pleae 
st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
        }
        )

def PlayBackMusicFile(FileLocation,FileType):
  # This function generate audio widget, replay the contents found in FileLocation
  # full specficaion for this widget can be found https://docs.streamlit.io/en/stable/api.html
  # This function requires file locaton and its type
  # I tried to find a way to run mid but failed.any help is appricated 
  audio_file = open(FileLocation, 'rb')
  audio_bytes = audio_file.read()
  st.audio(audio_bytes, format='audio/'+FileType)


st.markdown(""" <style> #MainMenu {visibility: hidden;} footer {visibility: hidden;} </style> """, unsafe_allow_html=True)
st.title("Interactive Music Composition Using Artifical Intelligence")
st.header("                                                   ")

#######################for one time only#############
st.write(os.getcwd())
us = music21.environment.UserSettings()
us_path = us.getSettingsPath()
if not os.path.exists(us_path):
    us.create()
us['musescoreDirectPNGPath'] = '/usr/share/sounds/sf3/default-GM.sf3'
st.write('Path to music21 environment', us_path)
st.write(us)
n = music21.note.Note('c')
#musicalNote=n.show('ipython.musicxml.png')
#from PIL import Image
#image = Image.open(musicalNote)
#st.image(image, caption='Sunrise by the mountains')


###################


MainPageDescription = st.empty()
MainPageDescription.write("""This is a beta version for an ambitious project aiming to promote the interactivity of 
         generate some musical pieces using Artificial Intelligence (AI) algorithms.
         Several AI models have been built and trained to match the variety of musical inputs ; furthermore, 
         the interface has been optimised to allow a user to add personal toutches and then to download the cratfed musical peices. 
         Wish this can aid the users to recogenise the potential rules that AI can play in art making. Source code is at:
         https://github.com/MohammedBaz/MusicStreamlit/blob/main/BackEndPrediction.py  
         """)

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
    MainPageDescription .empty() 
    add_selectbox=st.radio("you can upload your audio samples or use ours:", ("Upload some audio files", "Use some random Notes", "Use pretrainned Audios"),index=1)
if(add_selectbox=="Upload some audio files"):
  MainPageDescription .empty()       
  uploaded_file = MainPageDescription.file_uploader("Uplod AudioFile Here or leave it blank if other options are selected",
                                     type=['wav','mp3','mid'], accept_multiple_files=False, key=123456) 
  if uploaded_file is not None:                               # Just to check that the user has its own input to the filed_uploader
    if (uploaded_file.name.endswith('wav')):              # if the file is not mid, i.e., it is .wav or.mp3 then
        FileLocation=StoretheUpoldedFile(uploaded_file)         # Store the file and get its location information 
        FileType=FileLocation.split(".")[-1]
        PlayBackMusicFile(FileLocation,FileLocation.split(".")[-1]) # pass the locaiona and extension to PlayBackMusicFile to replay its contents
        from WaveFeatures import GetWavFeatures
        WavFeatures=GetWavFeatures(FileLocation)
        if (WavFeatures['NumberofSamples']<=0):
            st.error("It seems that the loaded file is corroupted, please upload another file")
    elif (uploaded_file.name.endswith('mid')):
        FileLocation=StoretheUpoldedFile(uploaded_file)
        midi_data = pretty_midi.PrettyMIDI(FileLocation)
        audio_data = midi_data.fluidsynth()
        audio_data = numpy.int16(
            audio_data / numpy.max(numpy.abs(audio_data)) * 32767 * 0.9
        )  # -- Normalize for 16 bit audio https://github.com/jkanner/streamlit-audio/blob/main/helper.py

        virtualfile = io.BytesIO()
        wavfile.write(virtualfile, 44100, audio_data)
        st.audio(virtualfile)
        
        
        
        FileLocation=StoretheUpoldedFile(uploaded_file)
        FileType=FileLocation.split(".")[-1]
        PlayBackMusicFile(FileLocation,FileLocation.split(".")[-1])
        
if(add_selectbox=="Use some random Notes"):
    GeneratemidFile(10)
    st.write(GeneratemidFile(10))
        
        
        
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
