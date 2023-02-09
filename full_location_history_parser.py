import os
import csv
import json
import datetime

def process_file(file_path, data_writer):
    with open(file_path, encoding='utf-8-sig') as file:
        data = json.load(file)
        try:
            for obj in data['locations']:
                if 'timestamp' in obj:
                    timestamp = obj['deviceTimestamp']
                    activity = obj.get('activity', [{"activity": "None"}])
                    activity = activity[0]["activity"]
                    max_confidence = 0
                    activity_type = ''
                    for act in activity:
                        if isinstance(act, dict) and act.get('confidence', 0) > max_confidence:
                            max_confidence = act['confidence']
                            activity_type = act['type']
                    try:
                        date_obj = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
                    except ValueError: 
                        date_obj = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
                    date_str = date_obj.strftime("%Y-%m-%d")
                    try:
                        datetime_obj = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
                    except ValueError:
                        datetime_obj = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
                    epoch_time = int(datetime_obj.timestamp())
                    try:
                        altitude = obj['altitude']
                    except KeyError:
                        altitude = 0
                    alt = altitude
                    sys_time = obj['timestamp']
                    platformtype = obj['platformType']
                    lat = obj['latitudeE7'] / 10**7
                    lon = obj['longitudeE7'] / 10**7
                    address = ""
                    placeid = ""
                    name = ""
                    data_writer.writerow([epoch_time, timestamp, date_str, lat, lon, address, placeid, name, alt, activity_type, platformtype, file_path, sys_time])
                    print('\r', timestamp + " latitude: " + str(lat) + " longitude: " + str(lon), end=" ")
        except KeyError:
            try:    
                for obj in data['timelineObjects']:
                    if 'placeVisit' in obj:
                        timestamp = obj['placeVisit']['duration']['startTimestamp']
                        try:
                            name = obj['placeVisit']['location']['name']
                        except KeyError:
                            name = obj['placeVisit']['location']['address']
                        try:
                            date_obj = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
                        except ValueError: 
                            date_obj = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
                        date_str = date_obj.strftime("%Y-%m-%d")
                        try:
                            datetime_obj = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
                        except ValueError:
                            datetime_obj = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
                        epoch_time = int(datetime_obj.timestamp())
                        lat = obj['placeVisit']['location']['latitudeE7'] / 10**7
                        lon = obj['placeVisit']['location']['longitudeE7'] / 10**7
                        address = obj['placeVisit']['location']['address']
                        placeid = obj['placeVisit']['location']['placeId']
                        alt = ""
                        activity_type = ""
                        platformtype = ""
                        sys_time = ""
                        data_writer.writerow([epoch_time, timestamp, date_str, lat, lon, address, placeid, name, alt, activity_type, platformtype, file_path, sys_time])
                        print('\r', timestamp + " latitude: " + str(lat) + " longitude: " + str(lon), end=" ")
            except KeyError:
                print('\r',end=" ")
                
        

def main():
    root_dir = "Takeout\Location History"
    output_file = "full_location_history.csv"

    with open(output_file, 'w', newline='') as outfile:
        data_writer = csv.writer(outfile)
        data_writer.writerow(["epoch_time", "timestamp", "date_str", "lat", "lon", "address", "placeid", "name", "alt", "activity_type", "platformtype", "file_path", "sys_time"])

        for subdir, dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith(".json") and file != "settings.json":
                    file_path = os.path.join(subdir, file)
                    process_file(file_path, data_writer)

if __name__ == "__main__":
    main()
    print('\n',end="full_location_history.csv created in current directory" )
