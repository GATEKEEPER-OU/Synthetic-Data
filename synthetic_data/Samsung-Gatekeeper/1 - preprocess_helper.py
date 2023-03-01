from pathlib import Path
import json

user = dict()
types = set()

userNo = 0

for p in Path('samsung_data/original').rglob('*'):
    if p.is_file():
        
        try:
            # Opening JSON file
            f = open(p)

            # returns JSON object as
            # a dictionary
            data = json.load(f)
        except:
            print(p)
            continue
        
        data.pop('data_source')
        data.pop('frequency')
        data.pop('user_uuid')
        data.pop('pilot_id')
        data.pop('timestamp')
        data.pop('time_offset')
        
        identifier = data['user_id']
        if identifier not in user:
            userNo = userNo + 1
            user[identifier] = userNo
                    
        data['user_id'] = 'User/' + str(user[identifier])   
        #print(data['user_id'])
        user_data = data['data']
                
        for u in user_data:
            u.pop('update_time')
            u.pop('day_time')
            u.pop('device_id')
            u.pop('data_uuid')
            
            if 'location_data' in u:
                u.pop('location_data')
                
            if 'parent_data_uuid' in u:
                u.pop('parent_data_uuid')
                
            #print(u['type_id'])
            types.add(u['type_id'])
            
            for v in u['values']:
                if 'end_time' in v:
                    v['end_time'] = '<' + str(int(v['end_time']) - int(v['start_time'])) + '>'
                v['start_time'] = '<' + str(int(v['start_time']) - 1000000000000) + '>'
                
            if 'binning_data' in u:
                for v in u['binning_data']:
                    v['end_time'] = '<' + str(int(v['end_time']) - int(v['start_time'])) + '>'
                    v['start_time'] = '<' + str(int(v['start_time']) - 1000000000000) + '>'
                    
            if 'live_data' in u:
                for v in u['live_data']:
                    v['end_time'] = '<' + str(int(v['end_time']) - int(v['start_time'])) + '>'
                    v['start_time'] = '<' + str(int(v['start_time']) - 1000000000000) + '>'

        filename = "samsung_data/working/observations.json"
        
        # Serializing json
        json_object = json.dumps(data)

        # Writing to file
        with open(filename, "a") as outfile:
            outfile.write(json_object + "\n")
