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
FileLocation = None
genetedNotes=None
################reconsidering pleae 
def GetWavFeatures(wav_file,OiginalWave): ##########
  SampleFrequecy, SoundArray = wavfile.read(wav_file)
  NormalisedSoundArray=SoundArray/numpy.iinfo(SoundArray.dtype).max 
  NumberofSamples=SoundArray.shape[0]
  if FileLocation==False:##################
    NumberofChannel=SoundArray.shape[1]###########
  else:###################################
    NumberofChannel=1
  DurationinSecond=NumberofSamples/SampleFrequecy
  TimePointArray=[]
  for i in range(NumberofSamples):
    x=(DurationinSecond/NumberofSamples)*i
    TimePointArray.append(x)
  FourierFrequencySpectrumAllChannels= numpy.abs(numpy.fft.rfft(NormalisedSoundArray))
  FrequencyPointArrayAllhannels = numpy.fft.rfftfreq(NormalisedSoundArray.size, d=1./SampleFrequecy)
  Allinformationdf = dict()
  Allinformationdf['SampleFrequecy'] = SampleFrequecy
  Allinformationdf['SoundArray'] = SoundArray
  Allinformationdf['NormalisedSoundArray'] = NormalisedSoundArray
  Allinformationdf['NumberofSamples'] = NumberofSamples
  Allinformationdf['NumberofChannel'] = NumberofChannel
  Allinformationdf['DurationinSecond'] = DurationinSecond
  Allinformationdf['TimePointArray'] = TimePointArray
  Allinformationdf['FourierFrequencySpectrumAllChannels'] = FourierFrequencySpectrumAllChannels
  Allinformationdf['FrequencyPointArrayAllhannels'] = FrequencyPointArrayAllhannels
  return (Allinformationdf)

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

def ChecktheCorrectnessofUploadedFile(uploaded_file):
    return
  
def parsemidfile(midfile):
  try:
    InputFile= pretty_midi.PrettyMIDI(midfile)
    st.write("time_signature_changes",InputFile.time_signature_changes)
    #st.write("estimate_tempi",estimate_tempo())
    ArrayedInputFile=[]
    for instrument in InputFile.instruments:
      for note in instrument.notes:
        Start=note.start
        End=note.end
        Pitch=note.pitch
        Velocity=note.velocity
        ArrayedInputFile.append([Start,End,Pitch,Velocity, instrument.program])
    #ArrayedInputFile = sorted(ArrayedInputFile, key=lambda x: (x[0], x[2]))# sorted the list based on the start and then pitch fields
    Allinformationdf=pandas.DataFrame(ArrayedInputFile, columns=['start','end','pitch','velocity','InstrumentNo'])
    
    StartBeat,Endbeat=[]
    for starttime in Allinformationdf['start']:
      StartBeat.append(InputFile.get_beats(starttime)[0])
    for endtime in Allinformationdf['end']:
      Endbeat.append(InputFile.get_beats(endtime)[0])
    ArrayedInputFile['startBeat']=StartBeat
    ArrayedInputFile['endBeat']=Endbeat  
    return (Allinformationdf)
  except:
    st.error('It seems that this is corrupted mod file, please upload another')
  
  
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

with st.sidebar.expander("The first step is listen to you"):
    MainPageDescription.empty() 
    add_selectbox=st.radio("Here you can:", ("Upload your audio files", "Generate musical Notes", "Use our pregeneraed Audios"),index=1)
if(add_selectbox=="Upload your audio files"):
  MainPageDescription.empty()       
  uploaded_file = MainPageDescription.file_uploader("Uplod AudioFile Here or leave it blank if other options are selected",type=['mid'], accept_multiple_files=False) 
  if uploaded_file is not None:                               # Just to check that the user has its own input to the filed_uploader
      st.write(parsemidfile(uploaded_file))
      
    #FileLocation=StoretheUpoldedFile(uploaded_file)         # Store the file and get its location information 
    #PlayBackMusicFile(FileLocation) # pass the locaiona and extension to PlayBackMusicFile to replay its contents
    #ChecktheCorrectnessofUploadedFile(uploaded_file)
    #GetWavFeatures(ConvertMiditoWave(FileLocation),false)
