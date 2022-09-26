# Synthetic Data Generator for MHR and Wearable data

This project aims to build a synthetic data generator (SDG) for the GATEKEEPER project (GK).
The SDG is developed in Python / Tensorflow.

The SDG trains different RNN models and can be used to generate a dataset about a cohort of synthetic patients for a number of days.

The architecture of the different RNN models had been tailored around as specific configutation of data.
These configuration correnspond to GK reference use cases, i.e., clinical studies involving a data collection combining, e.g., MHR, wearable biometric and behavioural data, and self-assessment surveys in the standard FHIR format.

## N.B. As is the case with any text generation Machine Learning model, a model trained to a high degree of accuracy can be used to reconstruct the training data. Therefore the trained model associated with this project should not be made available to those who have not been granted access to the original data.

## The project consists of 2 main parts:

1. Generator

The Generator is where the Data Generation process occurs.

The models used to generate text data were trained on approximately 186000 observations from a period of approximately 6 months. Approximately 123000 of the observations were related to sleep duration and 44000 to heart rate. The remaining observations were Floors climbed, Body height, Blood Pressure, "Glucose [Mass/volume] in Serum, Plasma or Blood", Fluid Intake, calories and exercise duration related to Walking, Swimmimg, Running, Bicycling and Steps in a 24 hour period. The models were trained for approximately 500 Epochs with each Epoch taking between 20 mins and 30 mins in a GPU environment.

The Generator requires access to a models directory.

The model directory should consist of:

model/timing_model.h5

model/event_model.h5

vocabulary/timings_vocab.json

vocabulary/events_vocab.json

codings/codings.csv

2. Evaluator

Various statistical analysis are carried out. Depending on the results the data is divided into "real" and "fake".

## Update 26/09/2022

Data can be now be gerenerated using a Transformer Model. This is in experimental mode, so deployment support is not available at this time. The Model uses a word level approach and thus does not perform as well, in terms of loss, as the RNN character level approach. However, generating data is a lot quicker. Training is ongoing. There will not be a separate Evaluator for the generated data. Instead the generated data will be evaluated against a Doc2Vec model, created from the Training data, using document similarity metrics. This is not a general mode. If evaluating please do so against the relevant Samsung Gatekeeper data.
