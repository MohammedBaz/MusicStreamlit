#################################################
# To do list: 
# 1- use music21 instead of pretty_midi in PlayBackMusicFile, so that all app use signal musical library, 
# the music21 is comptabile with lilypond which is used to display the musical note, but not with fluidsynth
# I think that pretty_midi stores notes in flat shape, but in music more sophesticated structure is used !!. 
# 
# 2-Typically, music21 uses musescore to render the musical notes, this requies to install the musescore on the device,
# in streamlit share, simply But it in packages.txt and then to add the path of musescore into the music21 environment
# file, a good describtion can be found here :https://www.audiolabs-erlangen.de/resources/MIR/FMP/C1/C1S2_SymbolicRendering.html. 
# In our case, the follwoing error raises music21.converter.subConverters.SubConverterException: Cannot find a path to the 'mscore' file at /usr/bin/mscore3 -- download MuseScore
# I left some of the code here as reminder for me:
# us = music21.environment.UserSettings()
# us_path = us.getSettingsPath()
# if not os.path.exists(us_path):
#    us.create()
# us['musescoreDirectPNGPath'] = '/usr/share/sounds/sf3/default-GM.sf3'
# st.write('Path to music21 environment', us_path)
# st.write(us)



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
from PIL import Image

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

def ConvertMiditoWave(FileLocation, samplerate=44100,AmplitudeQuantizationRange=16):
  midi_data = pretty_midi.PrettyMIDI(FileLocation)
  audio_data = midi_data.fluidsynth()## synthesizer the midi file, the output of this is a list of real numbers
  audio_data = numpy.int16(audio_data / numpy.max(numpy.abs(audio_data)) * 32767 ) # convert the synthesized numbers into another numbers between [-32767,32767]
  # this range represent 16bis which is selected here to reprsent the readings(amplitudes), other bits format 24 or 8 can be used instant. Some
  # referneces multiple the 32767 by 0.9 , e.g.,https://share.streamlit.io/andfanilo/streamlit-midi-to-wav/main/app.py whereas others like: 
  # https://stackoverflow.com/questions/10357992/how-to-generate-audio-from-a-numpy-array applied it without. I canot find a good reason for this multiplication, 
  # Populate the 16-bits audio data inthe memory, so it can be written to wave files  
  virtualfile = io.BytesIO()
  # 44100 is the sample_rate, other sample rate is also possible
  wavfile.write(virtualfile, 44100, audio_data)
  return (virtualfile)



def PlayBackMusicFile(FileLocation):
  # This function generate st.audio widget, replay the contents found in FileLocation
  # full specficaion for this widget can be found https://docs.streamlit.io/en/stable/api.html
  # This function pass the file to the widget directly, the extension extracted only as it is 
  # needed by tehs second argument of the st.audio widget  
  if FileLocation.endswith('wav'):
    audio_file = open(FileLocation, 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/'+FileLocation.split(".")[-1])
  # The st.audio widget cannot play mid file direclty, here there is a need to convert it to other format
  # wave is a good choice, the midi file consists of notes, instruments and many others; However, wav is simply 
  # an array of numbers.
  elif FileLocation.endswith('mid'):
    st.audio(ConvertMiditoWave(FileLocation))
  
def DisplayMusicalNotes(music): 
  # This function is used to render the musical sheet of the argument music
  # it is adopted from the idea presented in https://groups.google.com/g/music21list/c/kjjt3QucVFM
  # it is simply cast the music into strings and then to image.   
  streamingNotes=str(music.write('lily.png'))
  image = Image.open(streamingNotes)
  # Then the st.image widget is used to display the image
  st.image(image, caption='Musical sheet')

#################################################### page layout start here #########################################################

st.markdown(""" <style> #MainMenu {visibility: hidden;} footer {visibility: hidden;} </style> """, unsafe_allow_html=True)
st.title("Interactive Music Composition Using Artifical Intelligence")
st.header("                                                   ")
#One of the good widgets presented in streamlit is empty. it is a place holder so that we can consider it as template. 
MainPageDescription = st.empty()
MainPageDescription.write("""This is a beta version for an ambitious project aiming to promote the interactivity of 
         generate some musical pieces using Artificial Intelligence (AI) algorithms.
         Several AI models have been built and trained to match the variety of musical inputs ; furthermore, 
         the interface has been optimised to allow a user to add personal toutches and then to download the cratfed musical peices. 
         Wish this can aid the users to recogenise the potential rules that AI can play in art making. Source code is avaiavle free of charge at:
         https://github.com/MohammedBaz/MusicStreamlit/blob/main/BackEndPrediction.py.
         Suggestions and comments can be sent to mdbaz01@gmail.com 
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
        PlayBackMusicFile(FileLocation) # pass the locaiona and extension to PlayBackMusicFile to replay its contents
        from WaveFeatures import GetWavFeatures
        with open(FileLocation, "rb") as file:
            btn = st.download_button(label="Download your crafted file",
                                     data=file,
                                     file_name=FileLocation,
                                     mime='audio/'+FileLocation.split(".")[-1]
                                    )

        WavFeatures=GetWavFeatures(FileLocation)
        st.write(WavFeatures['SoundArray'].shape())
        if (WavFeatures['NumberofSamples']<=0):
            st.error("It seems that the loaded file is corroupted, please upload another file")
    elif (uploaded_file.name.endswith('mid')):
        FileLocation=StoretheUpoldedFile(uploaded_file)
        PlayBackMusicFile(FileLocation)
        
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
