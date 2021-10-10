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
  Trainingdataset=Prediction(Trainingdataset=Trainingdataset,modelname='StreamlitModel.h5',TrainingStep=1,PredicitonHorizontal=1)
#Generate midi file from the results:
def GenerateMidFile(OriginalandResult):
  midi = pretty_midi.PrettyMIDI() #define a new mid instance
  instrument = pretty_midi.Instrument(0) #use a single instrument for this instrument
  midi.instruments.append(instrument) #add this instrument to the mid file 
  for i in range(len(OriginalandResult)):
    notex = pretty_midi.Note(velocity=127,pitch=OriginalandResult[i],start=i, end=i+1)
    instrument.notes.append(notex)
  return(midi)
NewMid=GenerateMidFile(Trainingdataset+Trainingdataset)

with st.spinner(f"Transcribing to FluidSynth"):
        midi_data = pretty_midi.PrettyMIDI(NewMid)
        audio_data = midi_data.fluidsynth()
        audio_data = np.int16(
            audio_data / np.max(np.abs(audio_data)) * 32767 * 0.9
        )  # -- Normalize for 16 bit audio https://github.com/jkanner/streamlit-audio/blob/main/helper.py

        virtualfile = io.BytesIO()
        wavfile.write(virtualfile, 44100, audio_data)
st.audio(virtualfile)
st.markdown("Download the audio by right-clicking on the media player")

