import time

fhir_content = """
{
    "resourceType": "Bundle",
    "type": "transaction",
    "entry": [
        {
            "fullUrl": "https://www.gatekeeper-project.eu/sid/puglia/patient/001",
            "resource": {
                "resourceType": "Patient",
                "id": "001",
                "identifier": [
                    {
                        "system": "https://www.gatekeeper-project.eu/sid/puglia/identifier",
                        "value": "001"
                    }
                ]
            },
            "request": {
                "method": "POST",
                "url": "Patient",
                "ifNoneExist": "identifier=https://www.gatekeeper-project.eu/sid/puglia/patient|001"
            }
        },
        {
            "fullUrl": "https://www.gatekeeper-project.eu/sid/puglia/observation/MDAxMjAyMS0wMy0zMDI5",
            "resource": {
                "resourceType": "Observation",
                "id": "MDAxMjAyMS0wMy0zMDI5",
                "identifier": [
                    {
                        "system": "https://www.gatekeeper-project.eu/sid/puglia/identifier",
                        "value": "Observation/MDAxMjAyMS0wMy0zMDI5"
                    }
                ],
                "status": "final",
                "code": {
                    "coding": [
                        {
                            "system": "http://local-system",
                            "code": "patient_age",
                            "display": "Patient age"
                        }
                    ]
                },
                "subject": {
                    "reference": "https://www.gatekeeper-project.eu/sid/puglia/patient/001",
                    "display": "001"
                },
                "effectiveDateTime": "2021-03-30T00:00:00+02:00",
                "valueQuantity": {
                    "value": 29,
                    "unit": "year",
                    "system": "http://unitsofmeasure.org",
                    "code": "a_j"
                }
            },
            "request": {
                "method": "POST",
                "url": "Observation"
            }
        },
        {
            "fullUrl": "https://www.gatekeeper-project.eu/sid/puglia/observation/1234asdf-GlycosilatedEmoglobin",
            "resource": {
                "resourceType": "Observation",
                "id": "1234asdf-GlycosilatedEmoglobin",
                "identifier": [
                    {
                        "system": "https://www.gatekeeper-project.eu/sid/puglia/identifier",
                        "value": "Observation/1234asdf-GlycosilatedEmoglobin"
                    }
                ],
                "status": "final",
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "59261-8",
                            "display": "Hemoglobin A1c/Hemoglobin.total in Blood by IFCC protocol"
                        }
                    ]
                },
                "subject": {
                    "reference": "https://www.gatekeeper-project.eu/sid/puglia/patient/001",
                    "display": "001"
                },
                "effectiveDateTime": "2021-03-30T00:00:00+02:00",
                "valueQuantity": {
                    "value": 0.15090734,
                    "unit": "millimole per mole",
                    "system": "http://unitsofmeasure.org",
                    "code": "mmol/mol"
                },
                "hasMember": [
                    {
                        "reference": "https://www.gatekeeper-project.eu/sid/puglia/observation/MDAxMjAyMS0wMy0zMDI5",
                        "display": "MDAxMjAyMS0wMy0zMDI5"
                    }
                ]
            },
            "request": {
                "method": "POST",
                "url": "Observation"
            }
        }
    ]
}
"""

class SyntheticDataGenerator:

  def __init__(self, bundle_path):
    self.bundle_path = bundle_path

  def generate(self, output_dir: str, n_patients=1, n_days=1):
    filename = 'output-GlycosilatedEmoglobin.fhir.json'
    output_dir = output_dir.rstrip('/')
    path_filename = output_dir + '/' + filename
    # print(path_filename) # DEBUG
    fp = open(path_filename, 'w')
    fp.write(fhir_content)
    fp.close()
    time.sleep(5) # simulate a long job
