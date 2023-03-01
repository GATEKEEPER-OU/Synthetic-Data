import json
from genson import SchemaBuilder
from pathlib import Path

builder = SchemaBuilder()
for p in Path('samsung_data/original').rglob('*'):
    if p.is_file():
        with open(p, 'r') as f:
            try:
                datastore = json.loads(f.read())
                builder.add_object(datastore)
            except:
                print(p)

print(builder.to_schema())
print(builder.to_json(indent=2))
