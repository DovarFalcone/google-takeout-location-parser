import streamlit as st
import pandas as pd
import json
import datetime
import io
import zipfile

# Function to process uploaded files
def process_files(files):
    records = []
    
    for file in files:
        try:
            data = json.load(file)
            for obj in data.get('timelineObjects', []):
                if 'placeVisit' in obj and 'location' in obj['placeVisit']:
                    location = obj['placeVisit']['location']
                    address = location.get('address', 'Unknown')
                    name = location.get('name', address)
                    lat = location.get('latitudeE7', 0) / 10 ** 7
                    lon = location.get('longitudeE7', 0) / 10 ** 7
                    placeid = location.get('placeId', 'N/A')
                    
                    timestamp = obj['placeVisit'].get('duration', {}).get('startTimestamp')
                    epoch_time = None
                    if timestamp:
                        try:
                            datetime_obj = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
                        except ValueError:
                            datetime_obj = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
                        epoch_time = int(datetime_obj.timestamp())
                    
                    records.append([timestamp, lat, lon, address, placeid, name, epoch_time])
        except json.JSONDecodeError:
            st.error(f"Error processing file: {file.name}")
    
    return pd.DataFrame(records, columns=["timestamp", "latitude", "longitude", "address", "placeid", "name", "epoch_time"])

# Streamlit UI
st.title("Google Location History Parser")
st.write("Upload your Google Takeout location history folder (ZIP file) to process.")

uploaded_file = st.file_uploader("Choose a ZIP file", type=["zip"])

if uploaded_file is not None:
    st.write("Extracting and processing files...")
    with zipfile.ZipFile(uploaded_file, 'r') as z:
        json_files = [z.open(f) for f in z.namelist() if f.endswith('.json')]
        df = process_files(json_files)
    
    st.success("Files processed successfully!")
    
    # Display data preview
    st.subheader("Processed Data Preview")
    st.dataframe(df)
    
    # Display map
    st.subheader("Map View")
    st.map(df[['latitude', 'longitude']])
    
    # Provide CSV download
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_bytes = csv_buffer.getvalue().encode('utf-8')
    
    st.download_button(
        label="Download Processed Data as CSV",
        data=csv_bytes,
        file_name="semantic_location_history.csv",
        mime="text/csv"
    )
