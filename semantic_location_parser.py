import os
import csv
import json
import datetime

def process_file(file_path, data_writer):
    with open(file_path, encoding='utf-8-sig') as file:
        data = json.load(file)
        for obj in data['timelineObjects']:
            if 'placeVisit' in obj:
                try:
                    name = obj['placeVisit']['location']['name']
                except KeyError:
                    name = obj['placeVisit']['location']['address']
                lat = obj['placeVisit']['location']['latitudeE7'] / 10**7
                lon = obj['placeVisit']['location']['longitudeE7'] / 10**7
                timestamp = obj['placeVisit']['duration']['startTimestamp']
                address = obj['placeVisit']['location']['address']
                placeid = obj['placeVisit']['location']['placeId']
                
                # Convert the timestamp to a datetime object
                try:
                    datetime_obj = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
                except ValueError:
                    datetime_obj = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
                # Convert the datetime object to Unix epoch time
                epoch_time = int(datetime_obj.timestamp())
                
                # Write the data to the CSV file
                data_writer.writerow([timestamp, lat, lon, address, placeid, name, epoch_time])

def main():
    root_dir = "Takeout/Location History/Semantic Location History"
    output_file = "semantic_location_history.csv"

    with open(output_file, 'w', newline='') as outfile:
        data_writer = csv.writer(outfile)
        data_writer.writerow(["timestamp", "latitude", "longitude", "address", "placeid", "name", "epoch_time"])

        for subdir, dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith(".json"):
                    file_path = os.path.join(subdir, file)
                    process_file(file_path, data_writer)

if __name__ == "__main__":
    main()
    print('\n',end="semantic_location_history.csv created in current directory" )
