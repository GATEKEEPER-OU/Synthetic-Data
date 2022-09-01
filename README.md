# Synthetic Data Generator for MHR and Wearable data

This project aims to build a synthetic data generator (SDG) for the GATEKEEPER project (GK). 
The SDG is developed in Python / Tensorflow.

The SDG trains different RNN models and can be used to generate a dataset about a cohort of synthetic patients for a number of days.

The architecture of the different RNN models had been tailored around as specific configutation of data. 
These configuration correnspond to GK reference use cases, i.e., clinical studies involving a data collection combining, e.g., MHR, wearable biometric and behavioural data, and self-assessment surveys in the standard FHIR format.
