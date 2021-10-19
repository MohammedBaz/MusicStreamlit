


def ReshapeArrayTimeStepY(Inputarray,TimeStep):
  OutputArray=numpy.empty([len(Inputarray)-TimeStep,])
  for i in range(len(Inputarray)-TimeStep):
    OutputArray[i]=Inputarray[i+TimeStep]
  OutputArray=OutputArray.reshape(len(OutputArray),1)
  return OutputArray

def ReshapeArrayTimeStepX(Inputarray,TimeStep):
  OutputArray=numpy.empty([len(Inputarray)-TimeStep,TimeStep])
  for i in range(len(Inputarray)-TimeStep):
    OutputArray[i,:]=Inputarray[i:i+TimeStep]
  OutputArray=OutputArray.reshape(len(OutputArray),TimeStep,1)
  return OutputArray


def KerasAPImodel(TimeStep):
  from keras.layers import Input,Dense, concatenate,RepeatVector
  from keras.layers.recurrent import LSTM
  from keras.models import Model
  from tensorflow.keras.utils import plot_model
  
  AmplitudeInput=Input(shape=(TimeStep,1),name="AmplitudeInput")
  AmplitudeInputLSTM1=LSTM(100,activation='relu',return_sequences=True, name="AmplitudeInputLSTM1")(AmplitudeInput)
  AmplitudeInputLSTM2=LSTM(100,activation='relu',name="AmplitudeInputLSTM2")(AmplitudeInputLSTM1)
  AmplitudeInputDense1=Dense(100,name="AmplitudeInputDense1")(AmplitudeInputLSTM2)
  AmplitudeInputDense2=Dense(100,name="AmplitudeInputDense2")(AmplitudeInputDense1)
  
  ScaleInput=Input(shape=(TimeStep,1),name="ScaleInput")
  ScaleInputLSTM1=LSTM(100,activation='relu',return_sequences=True, name="ScaleInputLSTM1")(ScaleInput)
  ScaleInputLSTM2=LSTM(100,activation='relu',name="ScaleInputLSTM2")(ScaleInputLSTM1)
  ScaleInputDense1=Dense(100,name="ScaleInputDense1")(ScaleInputLSTM2)
  ScaleInputDense2=Dense(100,name="ScaleInputDense2")(ScaleInputDense1)
  
  Concatenated=concatenate([AmplitudeInputDense2,ScaleInputDense2],name="Concatenated")
  ConcatenatedReshape = RepeatVector(3,name="ConcatenatedReshape")(Concatenated)

  ConcatenatedLSTM1=LSTM(100,activation='relu',return_sequences=True, name="ConcatenatedLSTM1")(ConcatenatedReshape)
  ConcatenatedLSTM2=LSTM(100,activation='relu',name="ConcatenatedLSTM2")(ConcatenatedLSTM1)
  
  ConcatenatedDense1=Dense(100,name="ConcatenatedDense1")(ConcatenatedLSTM2)
  ConcatenatedDense2=Dense(100,name="ConcatenatedDense2")(ConcatenatedDense1)
  
  AmplitudeOutput=Dense(1,name="AmplitudeOutput")(ConcatenatedDense2)
  ScaleOutput=Dense(1,name="ScaleOutput")(ConcatenatedDense2)

  model=Model(inputs=[AmplitudeInput,ScaleInput], outputs=[AmplitudeOutput,ScaleOutput])
  #plot_model(model)
  #model.summary()

  model.compile(optimizer='adam', loss='mse')
  #model.fit([ReshapeArrayTimeStepX(Trainingdataset1,TimeStep),ReshapeArrayTimeStepX(Trainingdataset2,TimeStep)],
  #          [ReshapeArrayTimeStepY(Trainingdataset1,TimeStep), ReshapeArrayTimeStepY(Trainingdataset2,TimeStep)],
  #          epochs=50, verbose=0)
  return model


def HandMadeNormalisation(OriginalArray):
  OriginalArray=(OriginalArray-min(OriginalArray))/(max(OriginalArray)-min(OriginalArray))
  return OriginalArray



def Prediction(modelname,Trainingdataset1,Trainingdataset2,TimeStep,PredicitonHorizontal):
  from keras.models import load_model
  import numpy
  model =load_model(modelname)  # load the model 
  
  LengthofOriginalTrainingdataset=len(Trainingdataset1)
  OverallAmplitude=HandMadeNormalisation(numpy.array(Trainingdataset1))
  OverallScale=HandMadeNormalisation(numpy.array(Trainingdataset2))
  
  if(TimeStep !=2): # if the user attempts to change the timestep from 2 where the model is trained to other values then:
    ModifiedModel=KerasAPImodel(TimeStep) # create new model with the given 
    ModifiedModel.set_weights(model.get_weights())
    model=ModifiedModel
    
  for i in range(30):
    yhat=model.predict([OverallAmplitude[-TimeStep:].reshape(1,TimeStep,1),
                        OverallScale[-TimeStep:].reshape(1,TimeStep,1)])
    OverallAmplitude=numpy.append(OverallAmplitude, yhat[0])
    OverallScale=numpy.append(OverallScale, yhat[1])
  return (OverallAmplitude,OverallScale)



"""

import keras
from numpy import array

def Prediction(Trainingdataset,modelname='StreamlitModel.h5',TrainingStep=1,PredicitonHorizontal=1):
  model =keras.models.load_model(modelname)
  Predicitonresults=[]
  for i in range(PredicitonHorizontal):
    yhat=model.predict(array(Trainingdataset[-TrainingStep]).reshape(1,TrainingStep,1))
    Predicitonresults.append(int(yhat))
  return (Predicitonresults)
""" 
