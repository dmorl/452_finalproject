import pandas

file_name = 'sample_palm_data.txt'
palm_data = pandas.read_fwf(file_name, header=None)
# question for later: is there a way to automatically read in all files within a folder, or do you
# have to loop through a list of names or manually change the name each time?

# print(palm_data)

# put loaded data into dataframe
df = pandas.read_fwf(file_name, header=None)
# adding column names
df.columns = ["Time", "PDA ID", "Question ID", "Time to Respond*", "Answer ID", "Question Type", "Question Set ID", "Response"]
# print(df)
# PRINTING TAKES A LONG TIME...WHAT AM I DOING WRONG?
# print(type(df))
# print(df.dtypes)

# Isolate columns: Time, PDA ID, Question ID, Time to Respond, Response
# Double square brackets: first = action: subset column; second = list of columns to subset
df_working = df[['Time', 'PDA ID', 'Question ID', 'Time to Respond*', 'Response']]
# print(df_working)

# Use df_working.head() to only should first 5 rows instead of loading all the data each time
# print(df_working.head())

# Now split up column time into 2 sections: YYYYMMDD (reformatted into MM/DD/YYYY) and HHMMSS (into HH:MM:SS)
# Change the data type from int --> str
df_working['Time'] = df_working['Time'].astype(str)
# Now use split
df_working['Date_working'] = df_working['Time'].str[0:8]
df_working['Timestamp_working'] = df_working['Time'].str[8:14]
# print(df_working.head())

# Reformat
df_working['Date'] = pandas.to_datetime(df_working['Date_working'], format='%Y%m%d')
df_working['Timestamp'] = pandas.to_datetime(df_working['Timestamp_working'], format='%H%M%S')
# Removing date from timestamp
df_working['TimeStamp'] = pandas.Series([val.time() for val in df_working['Timestamp']])
# print(df_working.head())

# Change Time to Respond from 1/100 to x.xx format (divide by 100)
df_working['Time to Respond'] = df_working['Time to Respond*']/100

# Replace response values to only provide numeric value
# df_working['Response'] = df_working['Response'].map({"Yes ": 1, "No ": 0})
# df_working['Response'] = df_working['Response'].map({"a) more than 8 hours": 1, "b) 7-8 hours": 2, "c) 5-6 hours": 3,
#                                                      "d) 3-4 hours": 4, "e) 0-2 hours": 5})
# df_working['Response'] = df_working['Response'].map({"5 very poor": 5, "4 poor": 4, "3 fair": 3, "2 good": 2,
#                                                      "1 very good": 1})
# df_working['Response'] = df_working['Response'].map({"8 extremely": 8, "6 very much": 6, "4 much": 4, "2 somewhat": 2,
#                                                      "0 not at all": 0})
# df_working['Response'] = df_working['Response'].map({"8 the whole time": 8, "6 much": 6, "4 some": 4, "2 a little": 2})
# df_working['Response'] = df_working['Response'].map({"6 very": 6, "4 somewhat": 4})
# df_working['Response'] = df_working['Response'].map({"6 very": 6, "4 somewhat": 4})
# df_working['Response'] = df_working['Response'].map({"0 none": 0, "1 1-10min": 1, "2 11-20 min": 2, "3 21-30min": 3,
#                                                      "4 31-40min": 4, "5 41-50min": 5, "6 51-60min": 6, "7 61-70min": 7,
#                                                      "8 71-80min": 8})
# ...and this didn't work. Stack overflow has failed me!

# This also does not work --> I need to look over some more textbooks on pandas to figure this out
# df_working.Response[df_working.Response == 'Yes'] = 1


# New working dataset
df_working2 = df_working[['PDA ID', 'Date', 'TimeStamp', 'Question ID', 'Time to Respond', 'Response']]
print(df_working2.head())

# writing to an excel file
# but how exactly do I do this??
# outfile = open(file_name, 'w')
# pd.read_excel(file_name'.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
