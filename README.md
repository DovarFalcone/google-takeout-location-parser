# Location History Parser

This python script is used to parse Google Takeout Location History data into a csv file. The script can extract the `timestamp`, `address`, `placeId`, `name`, `latitudeE7` and `longitudeE7` values from the raw location history data and the semantic location history data and store them in a csv file. The resulting csv file can be used in ArcGIS for spatial analysis and visualization.

## Requirements
- Python 3.x
- pandas library

## Usage
1. Download and extract your Location History data from Google Takeout.
2. Save the script in the same folder as your Location History data.
3. Open a terminal/command prompt and navigate to the location of the script and the data.
4. Run the script using the command `python location_history_parser.py`.
5. The resulting csv file will be saved in the same folder as the script and data with the name `location_history.csv`.

## Data Format
Google Takeout Location History data consists of two types of data: raw location history data and semantic location history data.

```
E:.
|   location_history_parser.py
|
\---Takeout
    |   archive_browser.html
    |
    \---Location History
        |   Records.json
        |   Settings.json
        |   Tombstones.csv
        |
        \---Semantic Location History
            +---2022
            |       2022_DECEMBER.json
            |       2022_NOVEMBER.json
            |
            \---2023
                    2023_FEBRUARY.json
                    2023_JANUARY.json
```

The raw location history data is found in the `Records.json` file and consists of a single flat `locations` array containing all of the location records. A location record contains the following fields:
- `timestamp`: Timestamp of the record as a string in ISO 8601 format (YYYY-MM-DDTHH:mm:ss.sssZ). The suffixed Z indicates that the time is in the UTC time zone.
- `latitudeE7` and `longitudeE7`: Coordinates (latitude and longitude) of the location reported as integers. The values need to be divided by 107 to be in the expected range.

The semantic location history data is found in the `Semantic Location History` folder and consists of more high-level and processed information compared to the raw location history data. This data is partitioned by year in different subfolders and by month in different JSON files. Inside each semantic JSON file we can find a single flat `timelineObjects` array.

## Limitations
The script only extracts the `timestamp`, `address`, `placeId`, `name`, `latitudeE7` and `longitudeE7` values from the raw location history data and the semantic location history data and stores them in a csv file. If you need to extract additional information, you may need to modify the script accordingly.
