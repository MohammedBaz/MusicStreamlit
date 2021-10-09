import keras
from numpy import array

def Prediction(Trainingdataset,modelname='StreamlitModel.h5',TrainingStep=1,PredicitonHorizontal=1):
  model =keras.models.load_model(modelname)
  Predicitonresults=[]
  for i in range(PredicitonHorizontal):
    yhat=model.predict(array(Trainingdataset[-TrainingStep]).reshape(1,TrainingStep,1))
    Predicitonresults.append(int(yhat))
  return (Predicitonresults)
