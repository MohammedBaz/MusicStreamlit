import streamlit as st
import pretty_midi
import numpy as np 

st.title("AIMC")
st.header("Artificial Intelligence Music Composer")
from BackEndPrediction import Prediction
Trainingdataset=[]
uploaded_file = st.file_uploader("upload your mid file or leave blank for random startup", type="mid") #Add file uploader to take the user's input. limited to .png files only

def GenerateMidFile(OriginalandResult):
  midi = pretty_midi.PrettyMIDI() #define a new mid instance
  instrument = pretty_midi.Instrument(0) #use a single instrument for this instrument
  midi.instruments.append(instrument) #add this instrument to the mid file 
  for i in range(len(OriginalandResult)):
    notex = pretty_midi.Note(velocity=127,pitch=OriginalandResult[i],start=i, end=i+1)
    instrument.notes.append(notex)
  return(midi)


if uploaded_file is not None:
  midi_file = uploaded_file
  midi_data = pretty_midi.PrettyMIDI(midi_file)
  st.write( midi_data.estimate_tempo())
  for instrument in midi_data.instruments:
    # Don't want to shift drum notes
    if not instrument.is_drum:
        for note in instrument.notes:
            Trainingdataset.append(note.pitch)
  results=Prediction(Trainingdataset=Trainingdataset,modelname='StreamlitModel.h5',TrainingStep=1,PredicitonHorizontal=1) 
  #Generate midi file from the results:
  NewMid=GenerateMidFile(results+Trainingdataset)
  NewMid.write('newMid.mid')
  linko= f'<a href="data:application/octet-stream;{mid}" download="newMid.mid">Download midi file with save as</a>' 
  st.markdown(linko, unsafe_allow_html=True) 

