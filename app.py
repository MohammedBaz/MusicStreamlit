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
import time
from MidiFeatures import GetMidFeatures
import matplotlib.pyplot as plt

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
  #Then the st.image widget is used to display the image
  st.image(image, caption='Musical sheet')

def ChecktheCorrectnessofUploadedFile(uploaded_file):
    return
  
def parsemidfile(midfile):
  try:
    InputFile= pretty_midi.PrettyMIDI(midfile)
    st.write("time_signature_changes",InputFile.time_signature_changes)
    st.write('There are {} instruments'.format(len(InputFile.instruments)))
    st.write('Instrument 3 has {} notes'.format(len(InputFile.instruments[0].notes)))
    st.write('Instrument 4 has {} pitch bends'.format(len(InputFile.instruments[0].pitch_bends)))
    st.write('Instrument 5 has {} control changes'.format(len(InputFile.instruments[5].control_changes)))
    
    st.write("get_tempo_changes",len(InputFile.get_tempo_changes()))
    ArrayedInputFile=[]
    for instrument in InputFile.instruments:
      for note in instrument.notes:
        Start=note.start
        End=note.end
        Pitch=note.pitch
        Velocity=note.velocity
        #st.write(InputFile.get_beats(End)[0])
        ArrayedInputFile.append([Start,End,Pitch,Velocity, instrument.program])
    #ArrayedInputFile = sorted(ArrayedInputFile, key=lambda x: (x[0], x[2]))# sorted the list based on the start and then pitch fields
    Allinformationdf=pandas.DataFrame(ArrayedInputFile, columns=['start','end','pitch','velocity','InstrumentNo'])
    
    StartBeat=[]
    EndBeat=[]
    for starttime in Allinformationdf['start']:
      StartBeat.append(InputFile.get_beats(starttime)[0])
    Allinformationdf['startBeat']=StartBeat   
    return (Allinformationdf)
  except:
    st.error('It seems that this is corrupted mod file, please upload another')

    
def DisplayGeneralFeatrues(InputFile, WidgetControl=MainPageDescription):
  temp=GetMidFeatures(InputFile) 
  pm= pretty_midi.PrettyMIDI(InputFile)
  InstrumentName=[]
  for aInstrumentNo in numpy.unique(temp['InstrumentNo']):
    InstrumentName.append(pretty_midi.program_to_instrument_class(aInstrumentNo))
  FinalInstrumentName=numpy.unique(InstrumentName)
  if (widgetContrl is None):
    st.write('It is interesting truck of {} second'.format(int(pm.get_end_time())), 'It consists of {} notes'.format(temp.shape[0]),
             'it is played with the follwoing instrument(s) {}:'.format(FinalInstrumentName))
  else:
    WidgetControl.write('It is interesting truck of {} second'.format(int(pm.get_end_time())), 'It consists of {} notes'.format(temp.shape[0]),
             'it is played with the follwoing instrument(s) {}:'.format(FinalInstrumentName))
  
def PlotTempoChanges(InputFile):
  pm= pretty_midi.PrettyMIDI(InputFile)
  times, tempo_changes = pm.get_tempo_changes()
  fig, ax = plt.subplots()
  ax.plot(times, tempo_changes, '.')
  st.pyplot(fig)
  
def PlotPitchDistribution(InputFile):
  pm= pretty_midi.PrettyMIDI(InputFile)
  fig, ax = plt.subplots()
  plt.bar(numpy.arange(12), pm.get_pitch_class_histogram());
  ax.set_xticks(numpy.arange(12))
  ax.set_xticklabels(['C', '', 'D', '', 'E', 'F', '', 'G', '', 'A', '', 'B'])
  ax.set_xlabel('Musical Notes')
  ax.set_ylabel('Proportion')
  st.pyplot(fig)
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
    add_selectbox=st.radio("We can aid you to compete your piece: ", ("Upload your audio files", "Generate musical Notes", "Use our pregeneraed Audios"),index=1)
    if(add_selectbox=="Upload your audio files"):
      uploaded_file = MainPageDescription.file_uploader("Uplod AudioFile Here or leave it blank if other options are selected",type=['mid'], accept_multiple_files=False) 
      if uploaded_file is not None:                              # Just to check that the user has its own input to the filed_uploader
        FileLocation=StoretheUpoldedFile(uploaded_file)
        DisplayGeneralFeatrues(FileLocation)
        #with st.expander("Plot Tempo Changes"):
        #  PlotTempoChanges(FileLocation)
        #with st.expander("Plot Pitch Distrbution"):   
        #  PlotPitchDistribution(FileLocation)
        #with st.expander("Musical Sheet"):
        #  musictrack=music21.converter.parse(FileLocation)
        #  DisplayMusicalNotes(musictrack)
      
      
      
    #with st.expander("Harmony analysis"):
    #with st.expander("See explanation"):
    
    
    
  #    st.write(parsemidfile(uploaded_file))
      
    #FileLocation=StoretheUpoldedFile(uploaded_file)         # Store the file and get its location information 
    #PlayBackMusicFile(FileLocation) # pass the locaiona and extension to PlayBackMusicFile to replay its contents
    #ChecktheCorrectnessofUploadedFile(uploaded_file)
    #GetWavFeatures(ConvertMiditoWave(FileLocation),false)
