import streamlit as st
import pretty_midi
import numpy as np 
import pandas

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

def parsemidfile(midfile):
  InputFile= pretty_midi.PrettyMIDI(midfile)
  ArrayedInputFile=[]
  for instrument in InputFile.instruments:
    for note in instrument.notes:
      Start=note.start
      End=note.end
      Pitch=note.pitch
      Velocity=note.velocity
      ArrayedInputFile.append([Start,End,Pitch,Velocity, instrument.program])
  ArrayedInputFile = sorted(ArrayedInputFile, key=lambda x: (x[0], x[2]))# sorted the list based on the start and then pitch fields
  Allinformationdf=pandas.DataFrame(ArrayedInputFile, columns=['Start','duration','pitch','velocity','InstrumentNo'])
  return (Allinformationdf)


if uploaded_file is not None:
  midi_file = uploaded_file
  st.write(parsemidfile(midi_file))
  #Trainingdataset=np.array(parsemidfile(midi_file)[2])
  #midi_data = pretty_midi.PrettyMIDI(midi_file)
  #st.write( midi_data.estimate_tempo())
  #for instrument in midi_data.instruments:
    # Don't want to shift drum notes
    #if not instrument.is_drum:
        #for note in instrument.notes:
            #Trainingdataset.append(note.pitch)
  results=Prediction(Trainingdataset=Trainingdataset,modelname='StreamlitModel.h5',TrainingStep=1,PredicitonHorizontal=1) 
  #Generate midi file from the results:
  NewMid=GenerateMidFile(Trainingdataset+results)
  NewMid.write('newMid.mid')
  
 #https://discuss.streamlit.io/t/how-to-add-a-download-excel-csv-function-to-a-button/4474/6
  import os
  import base64
  def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href
  st.markdown(get_binary_file_downloader_html('newMid.mid', 'Audio'), unsafe_allow_html=True)
  #No way to play mid file!!
  
  audio_file = open('newMid.mid', 'rb')
  audio_bytes = audio_file.read()
  st.audio(audio_bytes, format='audio/mid')


 

 
