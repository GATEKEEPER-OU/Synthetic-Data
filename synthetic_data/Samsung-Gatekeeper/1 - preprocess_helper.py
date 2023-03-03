from pathlib import Path
import json
import ndjson
from datetime import datetime
import time
import os

def get_data_of_interest(filename:str, user_dict, day_order) :
    try:
        # Opening JSON file
        f = open(filename)

        # returns JSON object as a dictionary
        data = json.load(f)

        # Remove top level data that is not required
        outer_removals = ['data_source', 'frequency', 'user_uuid', 'pilot_id']
        for o_r in outer_removals:
            data.pop(o_r)

        # Replace user id with generated number
        identifier = data['user_id']
        if identifier not in user_dict:
            user_dict[identifier] = max(user_dict.values()) + 1

        data['user_id'] = 'User/' + str(user_dict[identifier])

        # Focus on user data
        type_ids = set()
        user_data = data['data']
        for u in user_data:
            # Save the type ids
            type_ids.add(u["type_id"])

            user_removals = ['update_time', 'day_time', 'device_id', 'data_uuid', \
                'location_data', 'parent_data_uuid', 'binning_data', 'live_data']

            for u_r in user_removals:
                if u_r in u:
                    u.pop(u_r)

            values = u['values']
            for v in values:
                if 'sleep_id' in v:
                    v.pop('sleep_id')

        type_ids = sorted(list(type_ids))
        types = {"type_ids": type_ids, "day_order": day_order}
        types.update(data)
        data = types
    except:
        # Something is wrong in the data
        data = None
    return data, user_dict


def anonymise_timestamps(data, start_time_adjustment:int):
    
    data['timestamp'] = '<' +  str(int(data['timestamp']) - start_time_adjustment) + '>'

    # For now only values
    user_data = data['data']

    # For now only values
    for u in user_data:
        values = u['values']
        for v in values:
            # For now, assume start_time always present
            if 'end_time' in v:
                # We set end_time to an interval so that we do not generate an end_time that is less than start_time
                v['end_time'] = '<' + str(int(v['end_time']) - int(v['start_time'])) + '>'
            v['start_time'] = '<' + str(int(v['start_time']) - start_time_adjustment) + '>'
    return data
    

if __name__ == "__main__":

    dataDir = r"samsung_data\original"
    newDataDir = r"samsung_data\values_only\\"
    
    # Start the user identifiers from 1001
    user_dict = {"Dummy": 1000}
    ndJSONlist = []

    for p in Path(dataDir).rglob('*'):
        if p.is_file():
            # Order of data. This isn't ideal but as the files are split into daily data
            # this is the only way of being able to generate more than 1 day for a single user
            # and keep the correlations. We should probably have another step that ensures that
            # the day_order starts at 1 and increments by 1 for each user, but let's see how this goes
            day_order = int(os.path.split(p.resolve().parent)[-1])
            
            # This value is for Github and script testing purposes
            day_order = day_order - 19700101

            data, user_dict = get_data_of_interest(p, user_dict, day_order)
            if data is None:
                continue

            # anonymise timestamps
            # This value is for Github and script testing purposes
            date_time = datetime(1970, 1, 1, 0, 0)

            # It appears that the timestamp in the raw data is in milliseconds
            time_adjustment = time.mktime(date_time.timetuple()) * 1000
            adj_data = anonymise_timestamps(data, int(time_adjustment))

            ndJSONlist.append(adj_data)

    output = ndjson.dumps(ndJSONlist)
    preprocessedFile = newDataDir + "observations.ndjson"
    
    #Writing to file
    with open(preprocessedFile, "w") as outfile:
            outfile.write(output)

    # Save for future refernce
    print(user_dict)
