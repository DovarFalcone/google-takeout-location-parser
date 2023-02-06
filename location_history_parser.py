import os
import json
import csv

def process_json(json_file):
    with open(json_file, "r") as f:
        data = json.load(f)
        timeline_objects = data["timelineObjects"]
        for obj in timeline_objects:
            place_visit = obj.get("placeVisit")
            if place_visit:
                latitude = place_visit["location"]["latitudeE7"] / 10**7
                longitude = place_visit["location"]["longitudeE7"] / 10**7
                yield [latitude, longitude]

def main():
    folder = "Takeout/Location History/Semantic Location History"
    result = []
    for year_folder in os.listdir(folder):
        year_folder_path = os.path.join(folder, year_folder)
        if os.path.isdir(year_folder_path):
            for json_file in os.listdir(year_folder_path):
                json_file_path = os.path.join(year_folder_path, json_file)
                if json_file_path.endswith(".json"):
                    result.extend(process_json(json_file_path))

    with open("location_history.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["latitude", "longitude"])
        writer.writerows(result)

if __name__ == "__main__":
    main()
