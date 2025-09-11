

# #pandas
# import pandas as pd
# #read csv
# df = pd.read_csv("/Users/rakeshnanankal/Downloads/Electric_Vehicle_Population_Data.csv")
# print(df.head())
# print(df.columns)
# #remove null values
# df = df.dropna()
# #data validation
# print(df.shape)
# print(df.dtypes)
# print(df.describe())
# print(df['Make'].unique())
# print(df['Make'].value_counts())
# #filtering
# tesla_cars = df[df['Make'] == 'TESLA']
# print(tesla_cars.count())
# #save to new csv

#regular expression
import regex as re

email = "rlkjdal@gak.com"
pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
if re.match(pattern, email):
    print("Valid email")
else:
    print("Invalid email")

#api
import requests
response = requests.get("https://jsonplaceholder.typicode.com/posts")
print(response.status_code)
print(response.json()[:1])  # Print the first post

