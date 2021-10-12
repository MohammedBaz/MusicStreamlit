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
