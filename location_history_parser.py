import os
import csv
import json
import datetime

def process_file(file_path, data_writer):
    with open(file_path, encoding='utf-8-sig') as file:
        data = json.load(file)
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
                # Write the data to the CSV file
                data_writer.writerow([epoch_time, timestamp, date_str, lat, lon, address, placeid, name])

def main():
    root_dir = "Takeout/Location History/Semantic Location History"
    output_file = "location_history.csv"

    with open(output_file, 'w', newline='') as outfile:
        data_writer = csv.writer(outfile)
        data_writer.writerow(["epoch_time", "timestamp", "date", "latitude", "longitude", "address", "placeid", "name"])

        for subdir, dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith(".json"):
                    file_path = os.path.join(subdir, file)
                    process_file(file_path, data_writer)

if __name__ == "__main__":
    main()
