# Synthetic Data Generator for MHR and Wearable data

This project aims to build synthetic data generator (SDG) models for the GATEKEEPER project (GK).

The architecture of the different models had been tailored around as specific configutation of data.
These configuration correnspond to GK reference use cases, i.e., clinical studies involving a data collection combining, e.g., MHR, wearable biometric and behavioural data, and self-assessment surveys in the standard FHIR format.

## N.B. As is the case with any text generation Machine Learning model, a model trained to a high degree of accuracy can be used to reconstruct the training data. Therefore the trained model associated with this project should not be made available to those who have not been granted access to the original data.


## Version 3 - Experimental Model - Transformer PT-1 (Generates and Evalutes data)

14/10/2022 - Code is no longer being updated. Exceptions are enhancements for deployment or high priority bug fixes.

Data can be now be gerenerated using a Transformer Model. There will not be a separate Evaluator for the generated data. Instead the generated data is evaluated against a Doc2Vec model, created from the Training data, using document similarity metrics. This is not a general model. If evaluating please do so against the relevant Samsung Gatekeeper data.

**Example of results**

{'code': {'coding': [{'code': '93829-0', 'display': 'REM sleep duration', 'system': 'http://loinc.org'}]}, 'status': 'preliminary', 'valuePeriod': {'end': '2022-Sep-20 05:43:47', 'start': '2022-Sep-20 05:36:47'}, 'resourceType': 'Observation'}

{'category': [{'coding': [{'code': 'vital-signs', 'display': 'Vital Signs', 'system': 'http://terminology.hl7.org/CodeSystem/observation-category'}], 'text': 'Vital Signs'}], 'code': {'coding': [{'code': '8867-4', 'display': 'Heart rate', 'system': 'http://loinc.org'}]}, 'effectiveDateTime': '2022-Sep-20 23:04:28', 'status': 'preliminary', 'valueQuantity': {'code': '/min', 'system': 'http://unitsofmeasure.org', 'unit': 'beats/minute', 'value': 79.0}, 'resourceType': 'Observation'}

{'code': {'coding': [{'code': '93830-8', 'display': 'Light sleep duration', 'system': 'http://loinc.org'}]}, 'status': 'preliminary', 'valuePeriod': {'end': '2022-Sep-23 20:30:47', 'start': '2022-Sep-23 20:28:47'}, 'resourceType': 'Observation'}

{'code': {'coding': [{'code': '93830-8', 'display': 'Light sleep duration', 'system': 'http://loinc.org'}]}, 'status': 'preliminary', 'valuePeriod': {'end': '2022-Sep-25 02:07:47', 'start': '2022-Sep-25 01:56:47'}, 'resourceType': 'Observation'}



## Version 2

The SDG trains different RNN models and is developed in Python / Tensorflow. It can be used to generate a dataset about a cohort of synthetic patients for a number of days.


### The project consists of 2 main parts:

1. Generator

The Generator is where the Data Generation process occurs.

The models used to generate text data were trained on approximately 186000 observations from a period of approximately 6 months. Approximately 123000 of the observations were related to sleep duration and 44000 to heart rate. The remaining observations were Floors climbed, Body height, Blood Pressure, "Glucose [Mass/volume] in Serum, Plasma or Blood", Fluid Intake, calories and exercise duration related to Walking, Swimmimg, Running, Bicycling and Steps in a 24 hour period. The models were trained for approximately 500 Epochs with each Epoch taking between 20 mins and 30 mins in a GPU environment.

The Generator requires access to a models directory.

The model directory should consist of:

- model/timing_model.h5
- model/event_model.h5
- vocabulary/timings_vocab.json
- vocabulary/events_vocab.json
- codings/codings.csv

2. Evaluator

Various statistical analysis are carried out. Depending on the results the data is divided into "real" and "fake".
