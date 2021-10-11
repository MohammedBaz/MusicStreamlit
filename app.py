import streamlit as st
import pretty_midi
import numpy as np 
import pandas
import os
import base64


st.title("AIMC")
st.header("Artificial Intelligence Music Composer")
from BackEndPrediction import Prediction
Trainingdataset=[]
#uploaded_file = st.file_uploader("upload your mid file or leave blank for random startup", type="mid") #Add file uploader to take the user's input. limited to .png files only

import pydub
from pathlib import Path

def upload_and_save_wavfiles(save_dir: str) -> List[Path]:
    """ limited 200MB, you could increase by `streamlit run foo.py --server.maxUploadSize=1024` """
    uploaded_files = st.file_uploader("upload", type=['wav', 'mp3'], accept_multiple_files=True)
    save_paths = []
    for uploaded_file in uploaded_files:
        if uploaded_file is not None:
            if uploaded_file.name.endswith('wav'):
                audio = pydub.AudioSegment.from_wav(uploaded_file)
                file_type = 'wav'
            elif uploaded_file.name.endswith('mp3'):
                audio = pydub.AudioSegment.from_mp3(uploaded_file)
                file_type = 'mp3'

            save_path = Path(save_dir) / uploaded_file.name
            save_paths.append(save_path)
            audio.export(save_path, format=file_type)
    return save_paths

def display_wavfile(wavpath):
    audio_bytes = open(wavpath, 'rb').read()
    file_type = Path(wavpath).suffix
    st.audio(audio_bytes, format=f'audio/{file_type}', start_time=0)


files = upload_and_save_wavfiles('temp')

for wavpath in files:
    display_wavfile(wavpath)

upload_and_save_wavfiles("/")








def GenerateMidFile(OriginalandResult):
  midi = pretty_midi.PrettyMIDI() #define a new mid instance
  instrument = pretty_midi.Instrument(0) #use a single instrument for this instrument
  midi.instruments.append(instrument) #add this instrument to the mid file 
  for i in range(len(OriginalandResult)):
    notex = pretty_midi.Note(velocity=127,pitch=min(OriginalandResult[i],127),start=i, end=i+1) # here min to limit those notes that generated by LSTM and more than 127 
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
  #ArrayedInputFile = sorted(ArrayedInputFile, key=lambda x: (x[0], x[2]))# sorted the list based on the start and then pitch fields
  Allinformationdf=pandas.DataFrame(ArrayedInputFile, columns=['Start','duration','pitch','velocity','InstrumentNo'])
  return (Allinformationdf)

def get_binary_file_downloader_html(bin_file, file_label='File'):
  with open(bin_file, 'rb') as f:
    data = f.read()
  bin_str = base64.b64encode(data).decode()
  href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
  return href

if uploaded_file is not None:
  x=[]
  x=parsemidfile(uploaded_file)['pitch']
  Trainingdataset=np.array(x)
  #midi_data = pretty_midi.PrettyMIDI(midi_file)
  #st.write( midi_data.estimate_tempo())
  #for instrument in midi_data.instruments:
    # Don't want to shift drum notes
    #if not instrument.is_drum:
        #for note in instrument.notes:
            #Trainingdataset.append(note.pitch)
  results=Prediction(Trainingdataset=Trainingdataset,modelname='StreamlitModel.h5',TrainingStep=1,PredicitonHorizontal=1) 
  #Generate midi file from the results:
  st.write(len(Trainingdataset),len(results))
  NewMid=GenerateMidFile(Trainingdataset+results)
  NewMid.write('newMid.mid')
  
 #https://discuss.streamlit.io/t/how-to-add-a-download-excel-csv-function-to-a-button/4474/6
  st.markdown(get_binary_file_downloader_html('newMid.mid', 'Audio'), unsafe_allow_html=True)
  
  #import io
  #encode_string = base64.b64encode(open('newMid.mid', 'rb').read())
  #st.audio(io.BytesIO(encode_string), format='audio/ogg', start_time=0)
  #bytestream = io.BytesIO('newMid.mid')
  #midi.writeFile(bytestream)
  #temp = io.BytesIO(bytestream.getvalue())
  #pygame.mixer.music.load(temp)
  #st.audio(temp, format='audio/ogg', start_time=0)
 


  #No way to play mid file!!
  
  #def GetParametersofMidforAudio(FileName):
  #  with open(FileName, 'rb') as f:
  #      data = f.read()
  #  bin_str = base64.b64encode(data).decode()
   # return(bin_str)
  
  #xxx=GetParametersofMidforAudio('newMid.mid')
  #audio_file = open('newMid.mid', 'rb')
  #audio_bytes = GetParametersofMidforAudio('newMid.mid')
  #st.audio(audio_bytes, format='audio/midi')
  #st.audio(data=GetParametersofMidforAudio('newMid.mid'), format='application/octet-stream', start_time=0)


 

 
