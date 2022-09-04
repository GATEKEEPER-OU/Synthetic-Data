import config
from config  import get_codings
import pandas as pd
import json
import glob
import os

# Get the csv files from the results directory
files = glob.glob(config.GENERATOR_RESULT_DIR + "/*.csv")

coding, display, guide_text = get_codings()

columns = ['Observation Time', 'Temperature', 'user', 'normTime', 'code', 'display', 'value', 'observation']

for filename in files:
    head, tail = os.path.split(filename)
    
    # Processed filename
    processedFile = os.path.join(config.GENERATOR_PROCESSED_DIR , tail)
    
    # Archive filename
    archiveFile = os.path.join(config.ARCHIVE_DIR, tail)

    # Processed Dataframe
    processedDF = pd.DataFrame(columns = columns)

    # reading content of csv files
    df = pd.read_csv(filename)
    df.rename(columns = {'Observation Time':'obsTime'}, inplace = True)

    # File should only contain 1 user and 1 temperature
    user = df.loc[0]['event'].split()[1]
    event_temperature = df.loc[0]['Temperature']

    for row in df.itertuples():
      code = row.event.split()[0]
      coding_index = coding.index(code)
      
      display1 = None
      obsJSON = None
      value = -1
      
      normTime = row.normTime
      obsTime = row.obsTime
      obs = " ".join(row.event.split()[3:])

      try:
          # Parse text to generate tabular data
          obsJSON = json.loads(obs.replace("\'", "\""))

          if "{'<duration>':" in guide_text[coding_index]:
            if 'valuePeriod' in obsJSON:
                value = obsJSON['valuePeriod']['<duration>']
          elif "'component': [" in guide_text[coding_index]:
                display1 = display[coding_index]
          elif 'valueQuantity' in obsJSON:
                value = obsJSON['valueQuantity']['value']
          else:
                print(obsJSON)
      except:
          pass

      if display1 is None:
          processedDF.loc[len(processedDF.index)] = [obsTime, event_temperature, user, normTime, code, display[coding_index], value, obs]
      else:
          if 'component' in obsJSON:
            component = obsJSON['component']
                  
            for compJSON in component:
                display2 = display1 + " - " + compJSON['display']
                
                if 'valueQuantity' in compJSON: 
                    value = compJSON['valueQuantity']['value']
                processedDF.loc[len(processedDF.index)] = [obsTime, event_temperature, user, normTime, code, display2, value, obs]

    try:
        processedDF.to_csv(processedFile, index=False)
        print(processedFile + " is ready for next stage")
        os.rename(filename, archiveFile)
    except:
        print(processedFile + " failed to be converted")