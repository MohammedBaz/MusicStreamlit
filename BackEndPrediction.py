
from keras.models import load_model
import numpy

def Prediction(modelname,Trainingdataset1,Trainingdataset2,TimeStep,PredicitonHorizontal):
  model =load_model(modelname)
  LengthofOriginalTrainingdataset=len(Trainingdataset1)
  Predicitonresults1=numpy.array(Trainingdataset1)
  Predicitonresults2=numpy.array(Trainingdataset2)
  for i in range(PredicitonHorizontal):
    yhat=model.predict([numpy.array(Predicitonresults1[-TimeStep:]).reshape(1,TimeStep,1),
                        numpy.array(Predicitonresults2[-TimeStep:]).reshape(1,TimeStep,1)])
    Predicitonresults1=numpy.append(Predicitonresults1, yhat[0])
    Predicitonresults2=numpy.append(Predicitonresults2, yhat[1])
  return (Predicitonresults1,Predicitonresults2)



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
