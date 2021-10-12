import numpy
from scipy.io import wavfile

def GetWavFeatures(wav_file):

  ## The input to this functon is the wavfile
  ## The output are : 
    # sampFreq is the sample frequency, i.e., the number of samples that are taken every second.
    # sound multi dimensional array containing the values of waves, 
    # the values of this array is a integer number [-2**number of bytes used to quantise the music,2**number of bytes used to quantise the music]
    # If number of dimension of SoundArray is 2 then the wav_file is of type stereo , one channel for the right speaker and other to the left, 
    # But if the number of dimension of SoundArray is 1, then the wav_file is of type mono. 
  SampleFrequecy, SoundArray = wavfile.read(wav_file)
    # NormalisedSoundArray conver the integer numbers in SoundArray into a flost within the ranges from [-1,1] 
  NormalisedSoundArray=SoundArray/numpy.iinfo(SoundArray.dtype).max #iinfo(SoundArray.dtype).max get the maximum values of the datatye of SoundArray, used to normaise the array 
    # number of readings in the wav file
  NumberofSamples=SoundArray.shape[0] 
    # number of chennals,  If number of dimension of SoundArray is 2 then the wav_file is of type stereo , one channel for the right speaker and other to the left, 
    # But if the number of dimension of SoundArray is 1, then the wav_file is of type mono. 
  NumberofChannel=SoundArray.shape[1]
    # Simply, we take 1/SampleFrequecy sampels everysecond since we have NumberofSamples samples then the duraion can be get as: 
  DurationinSecond=NumberofSamples/SampleFrequecy
    # Now we have a set of readings stored in SoundArray and the frequency with which these readings are sampled, i.e., SampleFrequecy readings are taken every second
    # from these two values we get the duration of the sound as above BUT we need also to get the time instant that is corrospding to each reading, for sure,
    # the first reading is located at 0, as Python starts at 0 and the last reading is set at DurationinSecond, BUT what about the intermediate readings?!. Nice the second 
    # reading is shifted by DurationinSecond/NumberofSamples from the first, the thrid is shifted by 2*DurationinSecond/NumberofSamples from the firs reading and so on:  
  TimePointArray=[]
  for i in range(NumberofSamples):
    x=(DurationinSecond/NumberofSamples)*i
    TimePointArray.append(x)
    # Now it is the time to move to freqquency domain: for the audio processing we need to calcaulte the amplitudes (those that are correpoding to readings of SoundArray)
    # As well as the FrequecyPoints( those that are corropsding to TimePointArray1). here we use:
    # np.fft.rfft to compute the abmplitude as our data readings of the sound is real not Complex 
  
  # FourierFrequencySpectrum is the Fourier transform of the signal, 
  # np.abs to treat the negative frequencies
  # np.fft.rfft is used as our data readings of the sound is real not Complex
  # Some Useful Sites: https://klyshko.github.io/teaching/2019-02-22-teaching
  # https://medium.com/@nadimkawwa/can-we-guess-musical-instruments-with-machine-learning-afc8790590b8 
  # Wave DataSet:https://magenta.tensorflow.org/datasets/nsynth

  FourierFrequencySpectrumAllChannels= numpy.abs(numpy.fft.rfft(NormalisedSoundArray))
  FrequencyPointArrayAllhannels = np.fft.rfftfreq(NormalisedSoundArray.size, d=1./SampleFrequecy)
  return(SampleFrequecy,SoundArray,NormalisedSoundArray,NumberofSamples,NumberofChannel,DurationinSecond,TimePointArray,FourierFrequencySpectrumAllChannels,FrequencyPointArrayAllhannels)
