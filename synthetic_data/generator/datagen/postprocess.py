import json
import pandas as pd
from datetime import datetime, timezone, timedelta
import logging
from fhir.resources.observation import Observation
from fhir.resources.bundle import Bundle

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def mappings(df, old_value, new_value):
    df['observation'] = df['observation'].str.replace(old_value, new_value, regex=True)
    return df


def transform(df):
    mapping_1 = [
                    ['"WALK 24"', '"Walking distance 24 hour Calculated"'],
                    ['"WALK SPEED 24"}', '"Walking speed 24 hour mean Calculated"'],
                    ['"STEPS 24"', '"Number of steps in 24 hour Measured"']
                ]

    mapping_2 = [
                    ['<URI_CSOC>', 'http://terminology.hl7.org/CodeSystem/observation-category'],
                    ['<URI_CSGK>', 'http://hl7.eu/fhir/ig/gk/CodeSystem/gatekeeper'],
                    ['<URI_SAMBG>', 'https://developer.samsung.com/health/server/partner-only/api-reference/data-types/blood-glucose.html'],
                    ['<URI_UOM>', 'http://unitsofmeasure.org'],
                    ['<URI_loinc>', 'https://loinc.org']
                ]

    for mapping in mapping_1:
        output = mappings(df, mapping[0], mapping[1])

    for mapping in mapping_2:
        output = mappings(output, mapping[0], mapping[1])

    return output


def convert_to_json(inputFile, userID):
    output = pd.read_csv(inputFile)
    output = output.sort_values(by='obsTime')
    output = transform(output)

    resource_list = []
    reject_list = []
    
    for time, data in zip(output['obsTime'], output['observation']):

        try:
            # JSON format
            json_data = json.loads(data)
            success = 0
        except:
            # Cannot format into JSON
            reject_list.append(data)
            logging.info('Cannot convert generated data to JSON: ' + str(userID))
            continue

        # We dropped status, subject and resourceType. Add these back in
        json_data["status"] = "final"
        json_data["subject"] = {"display": "Patient/" + str(userID), 
                            "reference": str(userID)}
        json_data["resourceType"] = "Observation"
    
        if "valuePeriod" in json_data:
            # Check for duration. Calculate start and end if possible
            if ("valuePeriod" in json_data) and ("<D>" in json_data["valuePeriod"]):
                value = json_data["valuePeriod"]['<D>']
                result = datetime.fromisoformat(time) - timedelta(seconds=value)
                result.isoformat(timespec='seconds')
                json_data["valuePeriod"]['start'] = result.isoformat(timespec='seconds')
                json_data["valuePeriod"]['end'] = time
                json_data["valuePeriod"].pop('<D>')

                success = 1
        elif "valueQuantity" in json_data:
            if "value" in json_data["valueQuantity"] and "effectiveDateTime" in json_data:
                if json_data["effectiveDateTime"] == '<EDT>':
                    json_data["effectiveDateTime"] = time
                    success = 1   
            elif "value" in json_data["valueQuantity"] and "effectiveTiming" in json_data:
                if 'event' in json_data["effectiveTiming"]:
                    if json_data["effectiveTiming"]['event'] == '<ET>':
                        json_data["effectiveTiming"]['event'] = time

                        success = 1
        elif "component" in json_data:
            corrupt = 0
            for comp in json_data["component"]:
                if "code" in comp and "valueQuantity" in comp:
                    if "value" not in comp["valueQuantity"]:
                        corrupt = 1
            if corrupt == 0:
                if 'effectiveDateTime' in json_data:
                    if json_data["effectiveDateTime"] == '<EDT>':
                        json_data["effectiveDateTime"] = time

                        success = 1

        if success == 0:
            # Either we have generated incorrect data or we have missed something
            # From time to time, the reject data should be checked.
            reject_list.append(json_data)
            logging.info('Error in generated data OR Case not accounted for: ' + str(userID))
            continue
        
        # Create FHIR observation
        obj = Observation.parse_raw(json.dumps(json_data))
        json_str = obj.json(indent=True)
        json_data = json.loads(json_str)
        resource = {"resource": json_data}
        resource_list.append(resource)

    if len(resource_list) == 0:
        json_data = None
    else:
        # Create FHIR bundle
        timeNow = datetime.now(timezone.utc).isoformat(timespec='seconds')
        bundle_data = {"entry": resource_list, "resourceType": "Bundle", "type": "batch-response", "timestamp": timeNow}
        obj = Bundle.parse_raw(json.dumps(bundle_data))
        json_str = obj.json(indent=True)
        json_data = json.loads(json_str)

    if len(reject_list) == 0:
        rejectDF = None
    else:
        rejectDF = pd.DataFrame(reject_list, columns=['Observation'])

    return json_data, rejectDF