# # import pandas as pd
# # import os
# # import glob

# # input_folder = r"D:\Data\Climate_Data_New"
# # output_folder = r"D:\Data\Climate_Data_Cleaned"

# # os.makedirs(output_folder, exist_ok=True)

# # keep_cols = [
# #     "STATION",
# #     "NAME",
# #     "LATITUDE",
# #     "LONGITUDE",
# #     "ELEVATION",
# #     "DATE",
# #     "SOURCE",
# #     "REPORT_TYPE",
# #     "DailyPrecipitation",
# #     "DailyAverageWindSpeed",
# #     "DailyPeakWindSpeed",
# #     "DailySustainedWindSpeed",
# #     "HourlyWindGustSpeed"
# # ]

# # rename_dict = {
# #     "STATION": "station_id",
# #     "NAME": "station_name",
# #     "LATITUDE": "latitude",
# #     "LONGITUDE": "longitude",
# #     "ELEVATION": "elevation",
# #     "DATE": "date",
# #     "SOURCE": "source",
# #     "REPORT_TYPE": "report_type",
# #     "DailyPrecipitation": "daily_precipitation",
# #     "DailyAverageWindSpeed": "daily_avg_wind_speed",
# #     "DailyPeakWindSpeed": "daily_peak_wind_speed",
# #     "DailySustainedWindSpeed": "daily_sustained_wind_speed",
# #     "HourlyWindGustSpeed": "hourly_wind_gust_speed"
# # }

# # files = glob.glob(os.path.join(input_folder, "*.csv")) + glob.glob(os.path.join(input_folder, "*.csv.gz"))

# # print(f"Total files found: {len(files)}")

# # for file in files:
# #     try:
# #         base_name = os.path.basename(file)
# #         if base_name.endswith(".csv.gz"):
# #             out_name = base_name.replace(".csv.gz", "_cleaned.csv")
# #         else:
# #             out_name = base_name.replace(".csv", "_cleaned.csv")

# #         out_path = os.path.join(output_folder, out_name)

# #         if os.path.exists(out_path):
# #             print(f"Skipped already cleaned file: {out_name}")
# #             continue

# #         first_chunk = True

# #         if file.endswith(".csv.gz"):
# #             reader = pd.read_csv(
# #                 file,
# #                 compression="gzip",
# #                 chunksize=10000,
# #                 engine="python"
# #             )
# #         else:
# #             reader = pd.read_csv(
# #                 file,
# #                 chunksize=10000,
# #                 engine="python"
# #             )

# #         for chunk in reader:
# #             existing_cols = [col for col in keep_cols if col in chunk.columns]
# #             df_clean = chunk[existing_cols].copy()
# #             df_clean.rename(columns=rename_dict, inplace=True)

# #             if first_chunk:
# #                 df_clean.to_csv(out_path, index=False, mode="w")
# #                 first_chunk = False
# #             else:
# #                 df_clean.to_csv(out_path, index=False, mode="a", header=False)

# #         print(f"Cleaned: {out_name}")

# #     except Exception as e:
# #         print(f"Error processing {file}")
# #         print(f"Reason: {e}")

# # import pandas as pd

# # df = pd.read_csv(r"D:\Data\Climate_Data_Cleaned\4248848_cleaned.csv")

# # print(df.head())
# # print(df.dtypes)
# # print(df["daily_precipitation"].describe())
# # print(df["daily_avg_wind_speed"].describe())
# # print(df["daily_peak_wind_speed"].describe())
# # print(df["hourly_wind_gust_speed"].describe())
# import pandas as pd
# # read dataset
# df = pd.read_csv(r"D:\Data\Climate_Data_Cleaned\4248848_cleaned.csv")
# df["daily_precipitation"] = pd.to_numeric(df["daily_precipitation"], errors="coerce")
# df["date"] = pd.to_datetime(df["date"])
# df["year"] = df["date"].dt.year
# print(df["daily_precipitation"].max())
# print(df["daily_precipitation"].describe())
# print(df[["date", "daily_precipitation"]].dropna().head(20))

# TIDE GUAGE DATA

# import requests
# import pandas as pd
# import os

# output_folder = r"D:\Data\Tide_Gauge_Metadata"
# os.makedirs(output_folder, exist_ok=True)

# meta_url = "https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations.json?type=waterlevels"

# data = requests.get(meta_url).json()
# stations = data["stations"]

# meta_df = pd.DataFrame(stations)

# meta_df = meta_df[["id", "name", "lat", "lng", "state"]].copy()
# meta_df = meta_df.rename(columns={
#     "id": "station_id",
#     "lat": "latitude",
#     "lng": "longitude"
# })

# print(meta_df.head())
# print(meta_df.shape)

# meta_df.to_csv(os.path.join(output_folder, "noaa_tide_station_metadata.csv"), index=False)
# print("Saved.")
# import arcpy
# arcpy.env.workspace = r"D:\Data"
# csv_file = r"d:\Data\Tide_Gauge_Metadata\noaa_tide_station_metadata.csv"
# output_points = r"D:\Data\stations_points.shp"
# if arcpy.Exists(output_points):
#     arcpy.management.Delete(output_points)
# arcpy.management.XYTableToPoint(
#     csv_file,
#     output_points,
#     "longitude",
#     "latitude",
#     coordinate_system=arcpy.SpatialReference(4326)
# )
# print("Station points created")
# import arcpy

# stations = r"D:\Data\stations_points.shp"
# counties = r"d:\Data\CZMP_counties_2009\CZMP_counties_2009.shp"
# output = r"D:\Data\stations_coastal.shp"

# arcpy.analysis.Intersect([stations, counties], output)

# print("Coastal stations extracted")
# import arcpy
# import pandas as pd
# import os

# coastal_stations = r"D:\Data\stations_coastal.shp"
# output_csv = r"D:\Data\coastal_station_ids.csv"

# # check field names first
# fields = [f.name for f in arcpy.ListFields(coastal_stations)]
# print("Fields:", fields)

# # usually the station field is called "station"
# rows = []
# with arcpy.da.SearchCursor(coastal_stations, ["station_id"]) as cursor:
#     for row in cursor:
#         rows.append(row[0])

# df = pd.DataFrame({"station_id": rows})
# df = df.drop_duplicates().reset_index(drop=True)

# df.to_csv(output_csv, index=False)

# print(df.head())
# print("Total unique stations:", len(df))
# print("Saved to:", output_csv)
# import arcpy

# arcpy.env.overwriteOutput = True
# input_shp = r"D:\Data\stations_coastal.shp"
# output_shp = r"D:\Data\stations_CONUS_GreatLakes.shp"
# keep_states = (
# "'CA','OR','WA',"
# "'TX','LA','MS','AL','FL',"
# "'GA','SC','NC','VA','MD','DE','NJ','NY','CT','RI','MA','NH','ME',"
# "'PA','OH','MI','IN','IL','WI','MN'"
#)
# where_clause = f"state IN ({keep_states})"
# arcpy.analysis.Select(input_shp, output_shp, where_clause)
# print("Filtered stations created")
# import arcpy
# import pandas as pd
# import os
# filtered_stations = r"D:\Data\stations_CONUS_GreatLakes.shp"
# output_csv = r"D:\Data\station_ids_CONUS_GreatLakes.csv"
# rows = []
# fields = [f.name for f in arcpy.ListFields(filtered_stations)]
# print("Fields:", fields)
# with arcpy.da.SearchCursor(filtered_stations, ["station_id", "name", "state"]) as cursor:
#     for row in cursor:
#         rows.append(row)
# df = pd.DataFrame(rows, columns=["station_id", "name", "state"])
# df = df.drop_duplicates().reset_index(drop=True)
# df.to_csv(output_csv, index=False)
# print(df.head())
# print("Total unique stations:", len(df))
# print("Saved to:", output_csv)

# import requests
# import pandas as pd

# station_id = "8771450"   # example
# year = 2000

# url = (
#     "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?"
#     f"begin_date={year}0101&end_date={year}1231"
#     f"&station={station_id}"
#     "&product=hourly_height"
#     "&datum=mllw"
#     "&units=metric"
#     "&time_zone=gmt"
#     "&application=research"
#     "&format=json"
# )

# response = requests.get(url, timeout=60)
# data = response.json()

# if "data" in data:
#     df = pd.DataFrame(data["data"])
#     df["station_id"] = station_id
#     df["year"] = year
#     print(df.head())
#     print(df.shape)
# else:
#     print(data)
import pandas as pd
import requests
import time
import os

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