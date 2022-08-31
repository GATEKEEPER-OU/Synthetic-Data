from dataGenModel import DataGenModel
import numpy as np

coding = '41950-7'
maxTimings = 100

temps = np.arange(0.0, 1.1, 0.1)

for temperature in temps:
    data_generator = DataGenModel(coding , maxTimings = maxTimings, eventTemperature = temperature)
    results_file = data_generator.generate_single_user()