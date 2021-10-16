import pretty_midi
import numpy
import pandas
#from google.colab import drive
#drive.mount('/content/gdrive')
#filename1='/content/gdrive/MyDrive/guitar/Arab1.mid'
#filename2='/content/gdrive/MyDrive/guitar/Arab2.mid'
#!pip install pretty_midi

def GetMidFeatures(InputFile):
  pm= pretty_midi.PrettyMIDI(InputFile)
  ArrayedInputFile=[]
  for instrument in pm.instruments:
    for anote in instrument.notes:
      Start=anote.start
      End=anote.end
      Pitch=anote.pitch
      Velocity=anote.velocity
      ArrayedInputFile.append([Start,End,Pitch,Velocity, instrument.program])
  NotesInformation=pandas.DataFrame(ArrayedInputFile, columns=['start','end','pitch','velocity','InstrumentNo'])
  return (NotesInformation)

def DisplayGeneralFeatrues(InputFile):
  temp=GetMidFeatures(InputFile) 
  pm= pretty_midi.PrettyMIDI(InputFile)
  InstrumentName=[]
  for aInstrumentNo in numpy.unique(temp['InstrumentNo']):
    InstrumentName.append(pretty_midi.program_to_instrument_class(aInstrumentNo))
  FinalInstrumentName=numpy.unique(InstrumentName)  
  print('It is interesting truck of {} second'.format(pm.get_end_time()), 'It consists of {} notes'.format(temp.shape[0]),
        'it is played with the follwoing instrument(s) {}:'.format(FinalInstrumentName), 
        )


 
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
  
