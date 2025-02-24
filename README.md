# Location History Parser

The Location History Parser offers a straightforward and efficient solution for anyone looking to analyze their Google Takeout location history data.

Downloading processed data as a CSV file opens up various possibilities for deeper analysis. Users can leverage tools like Excel, ArcGIS, or any other data analysis software to explore their data further, perform spatial analysis, and create custom visualizations.

While the provided scripts cover common use cases, they can be easily modified to extract additional data points or to suit specific analytical needs. This flexibility makes the tool suitable for both casual users and data enthusiasts.

## Requirements
- Python 3.x

## Streamlit App UPDATE

Try it yourself, hosted via streamlit. [Live Site](https://takeout-location-parser.streamlit.app/)

This Streamlit application (app.py) allows users to process and visualize their Google Takeout location history data. Users can upload a ZIP file containing their location history JSON files, and the app will extract, process, and display the data in an interactive format. The processed data can be downloaded as a CSV file for further analysis. You must have the Semantic Location History file present in order for this to run successfully.

Run the Streamlit app

1. `pip install -r requirements.txt`
2. `streamlit run app.py`

This will launch a web-based UI where you can upload your Google Takeout location history ZIP file and interact with the processed data.

![Fine Location data using app.py](/assets/images/streamlit.png)

## Manual Scripts

There are three scripts in this repo, `semantic_location_parser.py`, `records_location_parser.py`, and `full_location_history_parser.py`.

Each file scans through the Takeouts directory and parses the Google location data.

The resulting csv files can be used in ArcGIS for spatial analysis and visualization. If you want to see your data visually fast, then convert the csv to a macro enabled `.xlms` file and use Excel's mapping tool.

![Fine Location data using records_location_parser.py](/assets/images/airport.png)

## Usage
1. Download and extract your Location History data from [Google Takeout](https://takeout.google.com/). Google will send you a link to download a `.zip` file. Unzip the file into a new directory.
2. Save the python scripts in the same folder that you extracted the Takeouts folder.
3. Open a terminal/command prompt and navigate to the location of the script and the data.
4. Run the script using the command `python semantic_location_parser.py`.
5. The resulting csv file will be saved in the same folder as the script and data with the name `semantic_location_history.csv`.
6. The steps are the same for each script.

![File Location](/assets/images/filelocation.png)

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

The `semantic_location_parser.py` script is used to parse Google Takeout Location History data into a csv file. The script can extract the `timestamp`, `address`, `placeId`, `name`, `latitudeE7` and `longitudeE7` values from the semantic location history data and store them in a csv file. 

The semantic location history data is found in the `Semantic Location History` folder and consists of more high-level and processed information compared to the raw location history data found in the `records.json` file. This data is partitioned by year in different subfolders and by month in different JSON files. Inside each semantic JSON file we can find a single flat `timelineObjects` array.

The `records_location_parser.py` is used to pull the less refined location data that is collected. This data can be used to highlight what roads you traveled along rather than just what location you visited.

The `full_location_history_parser.py`parses the same data as the `semantic_location_parser.py`, but it also parses the `records.json` file in the same script. The two files are appended together on the `timestamp`, `lat`, and `lon` columns. It's not the best way to store this data and not adivsed to be used.

This data set will have the following columns:

- `epoch_time`: Useful for APIs
- `timestamp`: sample start time from device
- `date_str`: timestamp to date
- `lat`: latitudinal coordinate. The values need to be divided by 107 to be in the expected range.
- `lon`: logitudinal coordinate. The values need to be divided by 107 to be in the expected range.
- `address`: Best guess address by Google
- `placeid`: Google place id
-  `name`: Name of location if it exists
-  `alt`: altitude
- `activity_type`: Most confident activity type
- `platformtype`: Platform used to access Google services
- `file_path`: Which folder the data came from
- `sys_time`: Comes from the `timestamp` key in the `records.json`, unique.



## Limitations
The script only extracts specific values from the raw location history data and the semantic location history data and stores them in their respective csv files. If you need to extract additional information, you may need to modify the script accordingly.
