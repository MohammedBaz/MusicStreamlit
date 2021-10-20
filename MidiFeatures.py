import pretty_midi
import numpy
import pandas
import random
import os
from scipy.io import wavfile

def GetMidFeatures(InputFile):
  pm= pretty_midi.PrettyMIDI(InputFile)
  ArrayedInputFile=[]
  for instrument in pm.instruments:
    for anote in instrument.notes:
      Start=anote.start
      End=anote.end
      Duration=End-Start
      Pitch=anote.pitch
      Velocity=anote.velocity
      ArrayedInputFile.append([Start,End,Pitch,Velocity,Duration, instrument.program])
  NotesInformation=pandas.DataFrame(ArrayedInputFile, columns=['start','end','pitch','velocity','duration','InstrumentNo'])
  return (NotesInformation)


def GetNameofAllInstruments():
  InstrumentName=[]
  for i in range(127):
    InstrumentName.append(pretty_midi.program_to_instrument_name(i))
  return (numpy.unique(InstrumentName))

Tempos = [['Larghissimo', 1, 20], ['Grave', 20, 40], ['Slow', 40, 60],['Larghetto', 60, 66],['Adagio', 66, 76],['Adagietto', 70, 80],['Andante', 76, 108],
                ['Moderato',108, 120],['Allegro moderato', 112, 127],['Allegro', 120, 168],['Vivace', 168, 176],['Presto', 168, 200],['Prestissimo', 200, 176]]
Tempos = pandas.DataFrame(Tempos, columns = ['TempoName', 'MinValue','MaxValue'])

def aGenerateMidFile(MinTempo,MaxTempo, lenghtofMelody,listofInstruments):
  MinSelectedTempo=Tempos[Tempos['TempoName']==MinTempo].index[0]
  MaxSelectedTempo=Tempos[Tempos['TempoName']==MaxTempo].index[0]
  pm = pretty_midi.PrettyMIDI()
  velocity = 100
  startingPoint=0
  #inst.notes.append(pretty_midi.Note(velocity, random.choice(range(127)), start=0.0, end=EndingPoint))
  while(startingPoint<=lenghtofMelody):
      randomduration=random.uniform(1/(60*(Tempos['MinValue'][MinSelectedTempo])), 1/(60*(Tempos['MaxValue'][MaxSelectedTempo])))
      EndingPoint=randomduration+startingPoint
      #pretty_midi.Instrument(program=42,is_drum=False)
      randomInstrument=choice(listofInstruments)
      inst = pretty_midi.Instrument(program=pretty_midi.instrument_name_to_program(randomInstrument), is_drum=False,name=randomInstrument)
      pm.instruments.append(inst)
      inst.notes.append(pretty_midi.Note(velocity, random.choice(range(127)), start=startingPoint, end=EndingPoint))
      startingPoint=EndingPoint
  pm.write(os.path.join(os.getcwd(),"GeneratedFile.mid"))
  return(os.path.join(os.getcwd(),"GeneratedFile.mid"))

def ConvertMiditoWave(FileLocation, samplerate=44100,AmplitudeQuantizationRange=16):
  midi_data = pretty_midi.PrettyMIDI(FileLocation)
  audio_data = midi_data.fluidsynth()## synthesizer the midi file, the output of this is a list of real numbers
  audio_data = numpy.int16(audio_data / numpy.max(numpy.abs(audio_data)) * 32767 ) # convert the synthesized numbers into another numbers between [-32767,32767]
  # this range represent 16bis which is selected here to reprsent the readings(amplitudes), other bits format 24 or 8 can be used instant. Some
  # referneces multiple the 32767 by 0.9 , e.g.,https://share.streamlit.io/andfanilo/streamlit-midi-to-wav/main/app.py whereas others like: 
  # https://stackoverflow.com/questions/10357992/how-to-generate-audio-from-a-numpy-array applied it without. I canot find a good reason for this multiplication, 
  # Populate the 16-bits audio data inthe memory, so it can be written to wave files  
  #virtualfile = io.BytesIO()
  # 44100 is the sample_rate, other sample rate is also possible
  wavfile.write(os.path.join(os.getcwd(),'virtualfile.wave'), 44100, audio_data)
  return (os.path.join(os.getcwd(),'virtualfile.wave'))

def DisplayGeneralFeatrues(InputFile):
  temp=GetMidFeatures(InputFile) 
  pm= pretty_midi.PrettyMIDI(InputFile)
  InstrumentName=[]
  for aInstrumentNo in numpy.unique(temp['InstrumentNo']):
    InstrumentName.append(pretty_midi.program_to_instrument_class(aInstrumentNo))
  FinalInstrumentName=numpy.unique(InstrumentName)
  return(pm.get_end_time(),temp.shape[0],FinalInstrumentName)
  #st.write('It is interesting truck of {} second'.format(int(pm.get_end_time())),
  #         'It consists of {} notes'.format(temp.shape[0]),
  #         'it is played with the follwoing instrument(s) {}:'.format(FinalInstrumentName))


def bGenerateMidFile(listofPitches,listofTime):
  pm = pretty_midi.PrettyMIDI()
  velocity = 100
  startingPoint=0.0
  inst = pretty_midi.Instrument(program=pretty_midi.instrument_name_to_program('Electric Piano 1'))
  pm.instruments.append(inst)
  for i in range(len(listofPitches)):
    inst.notes.append(pretty_midi.Note(velocity, listofPitches[i], start=startingPoint, end=start+listofTime[i]))
    startingPoint=start+listofTime[i]
  pm.write(os.path.join(os.getcwd(),"Overall.mid"))
  return(os.path.join(os.getcwd(),"Overall.mid"))
 
##########################################













import music21
from random import randint, choice
import music21


def GetPossibleDuration():
  PossibleDuration=[4.0,3.0,3.5,2.0,4.0/3.0,1.0,2.0/3.0,1.5,1.75,0.5,0.75,1.0/3.0,
                    0.875,0.25,0.375,1.0/6.0,0.125,1.0/12.0] # this list in quarter lenght noation
  return(choice(PossibleDuration))

def GetPossibleNotenameWithOctave():
  listofInstrumentNos=GetInstrmentInformation(False)
  PossibleNotenameWithOctave=[]
  for i in range(127):
    notex=music21.note.Note(midi=i)
    for instrumentid in listofInstrumentNos:
      notex.midiProgram=instrumentid
      PossibleNotenameWithOctave.append(notex.nameWithOctave)
  return(numpy.unique(PossibleNotenameWithOctave))


def GetInstrmentInformation(gettheNumber):
  InstrumentName=[]
  InstrumentNumber=[]
  InstrumentNumberandName=[[]]
  for i in range (127): 
    try:# Not all numbers from 0 -127 can be used as instrument id, for exmple 2 gives error.
        #Morover some instrunment has more than id, e.g., Piano has 6 ids {0,2,3,4,5,6}
      bcl = music21.instrument.instrumentFromMidiProgram(i)
      InstrumentName.append(bcl.instrumentName)
      InstrumentNumber.append(i)
      InstrumentNumberandName.append([i, bcl.instrumentName])
    except:
      i=i+1
  if (gettheNumber):
    return(InstrumentNumber)
  else:
    return(InstrumentName)
  
  

def CreateNewNote(UsingMidiNumber,withduration,SpecificInstrument=None):
  #The main responsbility of this function is to generate a random note by setting  each of its attribute to a value within corrosping range:
  if (not (UsingMidiNumber)): # a note can be generated etiher by setting its midi number (an integer number within[0-127]) or musical symbols (e.g.,C#1) 
    randomNote=music21.note.Note(choice(GetPossibleNotenameWithOctave())) #to get a list of all musical symbols we write a function to iterate through all 
  else:                                                                   #notes and all instrument and them choise one of these list randomly.  
    randomNote=music21.note.Note(randint(0,127))                                                                                                                   
  if (withduration):
    randomNote.duration.quarterLength=GetPossibleDuration() #set the duration in quarter length
  randomNote.volume=127 #MIDI volume is the loudness of the entire instrument, while velocity is how hard a note is hit.
  randomNote.velocity=127 #here I set the values of both volume and velocity to the maximum values =127.
  if SpecificInstrument is not None:
    randomNote.midiProgram=choice(GetInstrmentInformation(True)) #set the insrument type  
  return(randomNote) 

def GeneratemidFile(LenghtofMelody):
  newchord=music21.chord.Chord()
  for i in range(LenghtofMelody):
    newchord.add(CreateNewNote(True,False,False))
    newchord.duration.quarterLength=GetPossibleDuration()
    newchord.show('text')
  return(newchord) 
  
