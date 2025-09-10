import pandas as pd

# Path to your CSV file
file_path = "/Users/rakeshnanankal/Downloads/Electric_Vehicle_Population_Data.csv"

# Read CSV into a Pandas DataFrame
df = pd.read_csv(file_path, delimiter=',', usecols=[0,2,3,4], nrows=100)

# Display the first 5 rows
print(df.iloc[8])
