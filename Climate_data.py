import pandas as pd
import os
import glob

# input_folder = r"D:\Data\Climate_Data_New"
# output_folder = r"D:\Data\Climate_Data_Cleaned"

# os.makedirs(output_folder, exist_ok=True)

# keep_cols = [
#     "STATION",
#     "NAME",
#     "LATITUDE",
#     "LONGITUDE",
#     "ELEVATION",
#     "DATE",
#     "SOURCE",
#     "REPORT_TYPE",
#     "DailyPrecipitation",
#     "DailyAverageWindSpeed",
#     "DailyPeakWindSpeed",
#     "DailySustainedWindSpeed",
#     "HourlyWindGustSpeed"
# ]

# rename_dict = {
#     "STATION": "station_id",
#     "NAME": "station_name",
#     "LATITUDE": "latitude",
#     "LONGITUDE": "longitude",
#     "ELEVATION": "elevation",
#     "DATE": "date",
#     "SOURCE": "source",
#     "REPORT_TYPE": "report_type",
#     "DailyPrecipitation": "daily_precipitation",
#     "DailyAverageWindSpeed": "daily_avg_wind_speed",
#     "DailyPeakWindSpeed": "daily_peak_wind_speed",
#     "DailySustainedWindSpeed": "daily_sustained_wind_speed",
#     "HourlyWindGustSpeed": "hourly_wind_gust_speed"
# }

# files = glob.glob(os.path.join(input_folder, "*.csv")) + glob.glob(os.path.join(input_folder, "*.csv.gz"))

# print(f"Total files found: {len(files)}")

# for file in files:
#     try:
#         base_name = os.path.basename(file)
#         if base_name.endswith(".csv.gz"):
#             out_name = base_name.replace(".csv.gz", "_cleaned.csv")
#         else:
#             out_name = base_name.replace(".csv", "_cleaned.csv")

#         out_path = os.path.join(output_folder, out_name)

#         if os.path.exists(out_path):
#             print(f"Skipped already cleaned file: {out_name}")
#             continue

#         first_chunk = True

#         if file.endswith(".csv.gz"):
#             reader = pd.read_csv(
#                 file,
#                 compression="gzip",
#                 chunksize=10000,
#                 engine="python"
#             )
#         else:
#             reader = pd.read_csv(
#                 file,
#                 chunksize=10000,
#                 engine="python"
#             )

#         for chunk in reader:
#             existing_cols = [col for col in keep_cols if col in chunk.columns]
#             df_clean = chunk[existing_cols].copy()
#             df_clean.rename(columns=rename_dict, inplace=True)

#             if first_chunk:
#                 df_clean.to_csv(out_path, index=False, mode="w")
#                 first_chunk = False
#             else:
#                 df_clean.to_csv(out_path, index=False, mode="a", header=False)

#         print(f"Cleaned: {out_name}")

#     except Exception as e:
#         print(f"Error processing {file}")
#         print(f"Reason: {e}")
# df = pd.read_csv(r"D:\Data\Climate_Data_Cleaned\4248848_cleaned.csv")

# print(df.head())
# print(df.dtypes)
# print(df["daily_precipitation"].describe())
# print(df["daily_avg_wind_speed"].describe())
# print(df["daily_peak_wind_speed"].describe())
# print(df["hourly_wind_gust_speed"].describe())
# import pandas as pd
# # read dataset
# df = pd.read_csv(r"D:\Data\Climate_Data_Cleaned\4248848_cleaned.csv")
# df["daily_precipitation"] = pd.to_numeric(df["daily_precipitation"], errors="coerce")
# df["date"] = pd.to_datetime(df["date"])
# df["year"] = df["date"].dt.year
# print(df["daily_precipitation"].max())
# print(df["daily_precipitation"].describe())
# print(df[["date", "daily_precipitation"]].dropna().head(20))

