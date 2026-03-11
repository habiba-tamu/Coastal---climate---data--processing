# TIDE GUAGE DATA

import requests
import pandas as pd
import os

output_folder = r"D:\Data\Tide_Gauge_Metadata"
os.makedirs(output_folder, exist_ok=True)

meta_url = "https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations.json?type=waterlevels"

data = requests.get(meta_url).json()
stations = data["stations"]

meta_df = pd.DataFrame(stations)

meta_df = meta_df[["id", "name", "lat", "lng", "state"]].copy()
meta_df = meta_df.rename(columns={
    "id": "station_id",
    "lat": "latitude",
    "lng": "longitude"
})

print(meta_df.head())
print(meta_df.shape)

meta_df.to_csv(os.path.join(output_folder, "noaa_tide_station_metadata.csv"), index=False)
print("Saved.")
import arcpy
arcpy.env.workspace = r"D:\Data"
csv_file = r"d:\Data\Tide_Gauge_Metadata\noaa_tide_station_metadata.csv"
output_points = r"D:\Data\stations_points.shp"
if arcpy.Exists(output_points):
    arcpy.management.Delete(output_points)
arcpy.management.XYTableToPoint(
    csv_file,
    output_points,
    "longitude",
    "latitude",
    coordinate_system=arcpy.SpatialReference(4326)
)
print("Station points created")
import arcpy

stations = r"D:\Data\stations_points.shp"
counties = r"d:\Data\CZMP_counties_2009\CZMP_counties_2009.shp"
output = r"D:\Data\stations_coastal.shp"

arcpy.analysis.Intersect([stations, counties], output)

print("Coastal stations extracted")
import arcpy
coastal_stations = r"D:\Data\stations_coastal.shp"
output_csv = r"D:\Data\coastal_station_ids.csv"

# # check field names first
fields = [f.name for f in arcpy.ListFields(coastal_stations)]
print("Fields:", fields)

# # usually the station field is called "station"
rows = []
with arcpy.da.SearchCursor(coastal_stations, ["station_id"]) as cursor:
    for row in cursor:
        rows.append(row[0])

df = pd.DataFrame({"station_id": rows})
df = df.drop_duplicates().reset_index(drop=True)

df.to_csv(output_csv, index=False)

print(df.head())
print("Total unique stations:", len(df))
print("Saved to:", output_csv)


arcpy.env.overwriteOutput = True
input_shp = r"D:\Data\stations_coastal.shp"
output_shp = r"D:\Data\stations_CONUS_GreatLakes.shp"
keep_states = (
"'CA','OR','WA',"
"'TX','LA','MS','AL','FL',"
"'GA','SC','NC','VA','MD','DE','NJ','NY','CT','RI','MA','NH','ME',"
"'PA','OH','MI','IN','IL','WI','MN'"
)
where_clause = f"state IN ({keep_states})"
arcpy.analysis.Select(input_shp, output_shp, where_clause)
print("Filtered stations created")


filtered_stations = r"D:\Data\stations_CONUS_GreatLakes.shp"
output_csv = r"D:\Data\station_ids_CONUS_GreatLakes.csv"
rows = []
fields = [f.name for f in arcpy.ListFields(filtered_stations)]
print("Fields:", fields)
with arcpy.da.SearchCursor(filtered_stations, ["station_id", "name", "state"]) as cursor:
    for row in cursor:
        rows.append(row)
df = pd.DataFrame(rows, columns=["station_id", "name", "state"])
df = df.drop_duplicates().reset_index(drop=True)
df.to_csv(output_csv, index=False)
print(df.head())
print("Total unique stations:", len(df))
print("Saved to:", output_csv)



# station_id = "8771450"   # example
# year = 2000

url = (
    "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?"
    f"begin_date={year}0101&end_date={year}1231"
    f"&station={station_id}"
    "&product=hourly_height"
    "&datum=mllw"
    "&units=metric"
    "&time_zone=gmt"
    "&application=research"
    "&format=json"
)

response = requests.get(url, timeout=60)
data = response.json()

if "data" in data:
    df = pd.DataFrame(data["data"])
    df["station_id"] = station_id
    df["year"] = year
    print(df.head())
    print(df.shape)
else:
    print(data)

import time


stations_file = r"D:\Data\station_ids_CONUS_GreatLakes.csv"
output_folder = r"D:\Data\Tide\tide_hourly"
os.makedirs(output_folder, exist_ok=True)

stations = pd.read_csv(stations_file)

for station_id in stations["station_id"].astype(str):

    print(f"\nDownloading station {station_id}")

    station_data = []

    for year in range(2000, 2026):

        url = (
            "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?"
            f"begin_date={year}0101&end_date={year}1231"
            f"&station={station_id}"
            "&product=hourly_height"
            "&datum=mllw"
            "&units=metric"
            "&time_zone=gmt"
            "&application=research"
            "&format=json"
        )

        try:
            r = requests.get(url, timeout=60)
            data = r.json()

            if "data" in data:
                df = pd.DataFrame(data["data"])
                df["station_id"] = station_id
                df["year"] = year
                station_data.append(df)
                print(f"{year} downloaded")
            else:
                print(f"{year} no data")

        except Exception as e:
            print(f"{year} error:", e)

        time.sleep(0.2)

    if station_data:
        station_df = pd.concat(station_data, ignore_index=True)
        out_file = os.path.join(output_folder, f"{station_id}.csv")
        station_df.to_csv(out_file, index=False)

        print("Saved:", out_file)