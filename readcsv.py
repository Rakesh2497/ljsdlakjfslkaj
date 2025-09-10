import pandas as pd


# Path to your CSV file
file_path = "/Users/rakeshnanankal/Downloads/Electric_Vehicle_Population_Data.csv"

# Read CSV into a Pandas DataFrame
df = pd.read_csv(file_path)

# Display the first 5 rows
print(df.head())
print(df.columns)
# Display the number of rows and columns
print(df.shape)
# Drop NaN values
df = df.dropna()
# Display the number of rows and columns after dropping NaN values
print(df.shape)
# Display data types of each column
print(df.dtypes)
# Display summary statistics
print(df.describe())
# Display unique values in a specific column (e.g., 'Make')
print(df['Make'].unique())
# Display the count of unique values in a specific column (e.g., 'Make')
print(df['Make'].value_counts())
# Filter rows based on a condition (e.g., 'Make' is 'TESLA')
tesla_cars = df[df['Make'] == 'TESLA']
print(tesla_cars.count())




