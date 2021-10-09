import streamlit as st

import pretty_midi

st.title("AIMC")
st.header("Artificial Intelligence Music Composer")
from BackEndPrediction import Prediction

uploaded_file = st.file_uploader("upload your mid file or leave blank for random startup", type="mid") #Add file uploader to take the user's input. limited to .png files only
if uploaded_file is not None:
  Trainingdataset=[]
  midi_file = uploaded_file
  midi_data = pretty_midi.PrettyMIDI(midi_file)
  st.write( midi_data.estimate_tempo())
  for instrument in midi_data.instruments:
    # Don't want to shift drum notes
    if not instrument.is_drum:
        for note in instrument.notes:
            Trainingdataset.append(note.pitch)
  result=Prediction(Trainingdataset=Trainingdataset,modelname='StreamlitModel.h5',TrainingStep=1,PredicitonHorizontal=1)
  st.write(result)
  st.write("## Audio file example")
  audio_file = open(result, "rb")
  st.audio(audio_file.read())
