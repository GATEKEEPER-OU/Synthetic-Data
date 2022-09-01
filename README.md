# Synthetic Data Generator for MHR and Wearable data

This project aims to build a synthetic data generator (SDG) for the GATEKEEPER project (GK). 
The SDG is developed in Python / Tensorflow.

The SDG trains different RNN models and can be used to generate a dataset about a cohort of synthetic patients for a number of days.

The architecture of the different RNN models had been tailored around as specific configutation of data. 
These configuration correnspond to GK reference use cases, i.e., clinical studies involving a data collection combining, e.g., MHR, wearable biometric and behavioural data, and self-assessment surveys in the standard FHIR format.

The project consists of 3 main parts

1. Generator

The Generator is where the Data Generation process occurs. 

The models used to generate text data were trained on approximately 186000 observations from a period of approximately 6 months. Approximately 123000 of the observations were related to sleep duration and 44000 to heart rate. The remaining observations were Floors climbed, Body height, Blood Pressure, "Glucose [Mass/volume] in Serum, Plasma or Blood", Fluid Intake, calories and exercise duration related to Walking Swimmimg, Running, Bicycling and Steps in a 24 hour period.

The output from the Generator, which is sent to Middleware is in a compressed FHIR format.

2. Middleware

The purpose of the Middleware layer is to reformat the generated data and to transfer the data in a secure manner to downstream systems. For example, the code in the Middleware layer converts the compressed FHIR from Generation into tabular format and transfers this data to Evaluation so that statistical analysis could be carried out 

3. Evaluation

Various statistical analysis are carried out. Depending on the results the data is divided into "real" and "fake". This information is passed back to the Middleware layer.
