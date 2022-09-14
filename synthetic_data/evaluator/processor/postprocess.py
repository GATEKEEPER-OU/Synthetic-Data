
def postprocess(input_dir: str, output_dir: str):
    # Hastily done. Mappings should be treated as static
    import glob
    import os
    import pandas as pd
    from datetime import datetime, timedelta

    floor_climbed = "code': {'coding': [{'code': 'floor-climbed', 'Floors climbed', 'system': '<GK>'}]}, 'effectiveDateTime': '<observationTime>"
    heart_rate = "category': <Vital_Signs>, 'text': 'Vital Signs'}], 'code': {'coding': [{'code': '8867-4', 'Heart rate', 'system': '<loinc>'}]}, 'effectiveDateTime': '<observationTime>"
    no_display_85354_9 = "category': <Vital_Signs>, 'text': 'Vital Signs'}], 'code': {'coding': [{'code': '85354-9', 'system': '<loinc>'}]}"
    blood_pressure_1 = "code': {'coding': [{'code': '8480-6', 'Systolic blood pressure', 'system': '<loinc>'}]}"
    blood_pressure_2 = "code': {'coding': [{'code': '8462-4', 'Diastolic blood pressure', 'system': '<loinc>'}]}"
    caffeine_intake_est = "code': {'coding': [{'code': '80489-8', 'Caffeine intake 24 hour Estimated', 'system': '<loinc>'}]}, 'effectiveDateTime': '<observationTime>"
    fluid_intake = "code': {'coding': [{'code': '9108-2', 'Fluid intake total 24 hour', 'system': '<loinc>'}]}, 'effectiveDateTime': '<observationTime>"
    sleep_duration_1 = "code': {'coding': [{'code': '93830-8', 'Light sleep duration', 'system': '<loinc>'}]}"
    sleep_duration_2 = "code': {'coding': [{'code': 'LP412113-5', 'Light sleep duration', 'system': '<loinc>'}]}"
    sleep_duration_3 = "code': {'coding': [{'code': '93831-6', 'Deep sleep duration', 'system': '<loinc>'}]}"
    sleep_duration_4 = "code': {'coding': [{'code': '93829-0', 'REM sleep duration', 'system': '<loinc>'}]}"
    sleep_duration_5 = "code': {'coding': [{'code': '93832-4', 'Sleep duration', 'system': '<loinc>'}]}"
    walking_activity = "code': {'coding': [{'code': '73985-4', 'Exercise activity', 'system': '<loincs>'}, {'code': 'LA11834-1', 'Walking', 'system': '<loinc>'}]}"
    bicycling_activity = "code': {'coding': [{'code': '73985-4', 'Exercise activity', 'system': '<loincs>'}, {'code': 'LA11837-4', 'Bicycling', 'system': '<loinc>'}]}"
    swimming_activity = "code': {'coding': [{'code': '73985-4', 'Exercise activity', 'system': '<loincs>'}, {'code': 'LA11838-2', 'Swimming', 'system': '<loinc>'}]}"
    running_activity = "code': {'coding': [{'code': '73985-4', 'Exercise activity', 'system': '<loincs>'}, {'code': 'LA11836-6', 'Running', 'system': '<loinc>'}]}"
    exercise_duration = "code': {'coding': [{'code': '55411-3', 'Exercise duration', 'system': '<loinc>'}]}"
    calories = "code': {'coding': [{'code': '41981-2', 'Calories burned', 'system': '<loinc>'}]}"
    steps_1 = "code': {'coding': [{'code': '41950-7', 'Number of steps in 24 hour Measured', 'system': '<loincs>'}]}"
    steps_2 = "code': {'coding': [{'code': '41950-7', 'Number of steps in 24 hour Measured', 'system': '<loinc>'}]}"
    walking_speed = "code': {'coding': [{'code': '41957-2', 'Walking speed 24 hour mean Calculated', 'system': '<loinc>'}]}"
    walking_distance = "code': {'coding': [{'code': '41953-1', 'Walking distance 24 hour Calculated', 'system': '<loinc>'}]}"
    height = "code': {'coding': [{'code': '8302-2', 'Body height', 'system': '<loinc>'}]}, 'effectiveDateTime': '<observationTime>"
    glucose = "code': {'coding': [{'code': '74774-1', 'Glucose [Mass/volume] in Serum, Plasma or Blood', 'system': '<loinc>'}]}"

    # Columns for ouput dataframe
    columns = ['obsTime', 'start', 'end', 'Temperature', 'text', 'value', 'observation']

    # Get the csv files from the real directory
    files = glob.glob(input_dir + "/*.csv")

    for filename in files:
        _, tail = os.path.split(filename)
    
        # Processed filename
        processedFile = os.path.join(output_dir, tail)

        # Processed Dataframe
        processedDF = pd.DataFrame(columns = columns)

        # reading content of csv files
        df = pd.read_csv(filename)

        for row in df.itertuples():
            coding = row.coding
            line = row.display
            obsTime = row.obsTime
            value = row.value
            observation = row.observation
            temperature = row.Temperature

            if coding == 'floor-climbed':
                line = line.replace("Floors climbed", floor_climbed)
            elif coding == '8867-4':
                line = line.replace("Heart rate", heart_rate)
            elif coding == '85354-9':
                line = line.replace("Blood", no_display_85354_9)
                line = line.replace("Systolic blood pressure", blood_pressure_1)
                line = line.replace("Diastolic blood pressure", blood_pressure_2)
            elif coding == '80489-8':
                line = line.replace("Caffeine intake 24 hour Estimated", caffeine_intake_est)
            elif coding == '9108-2':
                line = line.replace("Fluid intake total 24 hour", fluid_intake)
            elif coding == '93830-8':
                line = line.replace("Light sleep duration", sleep_duration_1)
            elif coding == 'LP412113-5':
                line = line.replace("Light sleep duration", sleep_duration_2)
            elif coding == '93831-6':
                line = line.replace("Deep sleep duration", sleep_duration_3)
            elif coding == '93829-0':
                line = line.replace("REM sleep duration", sleep_duration_4)
            elif coding == '93832-4':
                line = line.replace("Sleep duration", sleep_duration_5)
            elif coding == 'LA11834-1':
                line = line.replace("Walking", walking_activity)
            elif coding == 'LA11837-4':
                line = line.replace("Bicycling", bicycling_activity)
            elif coding == 'LA11838-2':
                line = line.replace("Swimming", swimming_activity)
            elif coding == 'LA11836-6':
                line = line.replace("Running", running_activity)
            elif coding == '8302-2':
                line = line.replace("Body height", height)
            elif coding == '74774-1':
                line = line.replace("Glucose [Mass/volume] in Serum, Plasma or Blood", glucose)
        
            line = line.replace("Exercise duration", exercise_duration)
            line = line.replace("Calories burned", calories)
            line = line.replace("Number of steps in 24 hour Measured 1", steps_1)
            line = line.replace("Number of steps in 24 hour Measured 2", steps_2)
            line = line.replace("Walking speed 24 hour mean Calculated", walking_speed)
            line = line.replace("Walking distance 24 hour Calculated", walking_distance)

            end = None
            start = None

            if '<duration>' in observation: 
                format = "%Y-%b-%d %X"
                dt_object = datetime.strptime(obsTime, format)
            
                end = obsTime
                # obsTime = None
                start = dt_object - timedelta(seconds=int(value))
                start = start.strftime("%Y-%b-%d %X")

            processedDF.loc[len(processedDF.index)] = [obsTime, start, end, temperature, line, value, observation]

        processedDF = processedDF.pivot(index=['obsTime', 'start', 'end', 'Temperature', 'value'], columns= ['text'], values =['observation'])
        processedDF = processedDF['observation'].reset_index()

        processedDF.to_csv(processedFile, index = False) 