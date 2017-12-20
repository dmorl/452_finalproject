## Convert it all to a CSV for pure python

# Importing pandas to create a dataframe to export as a .csv
# This will make it easier to extract data than working within a .txt document
import pandas as pd

# Import the .txt document, and read in assigning headers
file_name = 'sample_palm_data.txt'
palm_data = pd.read_fwf(file_name, header=None)


palm_data.columns = ["Time", "PDA ID", "Question ID", "Time to Respond*", "Answer ID", "Question Type",
					 "Question Set ID", "Response"]
# cols
# ["Time", "PDA ID", "Question ID", "Time to Respond*",
#  "Answer ID", "Question Type", "Question Set ID", "Response"]

# Save as .csv, with temporary to indicate that this isn't the final version
temporary_csv = file_name.replace(".txt", "TEMP.csv")
palm_data.to_csv(temporary_csv, index = False)


## now do stuff
# Read in the .csv document that was just created
import csv

with open(temporary_csv, 'r') as fin:
	io = csv.reader(fin)
	headers = next(io)
	data = [r for r in io]

data_fixed_dates = []

## split out the date and time
# Loop over each row within the dataset to split out the date and time, and also format them correctly
# Add the corrected date and time to the dataset
for row in data:
	date_working = row[0][:8]
	date = date_working[0:4] + "-" + date_working[4:6] + "-" + date_working[6:9]
	time_working = row[0][8:]
	time = time_working[0:2] + ":" + time_working[2:4] + ":" + time_working[4:6]
	data_fixed_dates.append([date, time] + row[1:])

# Create a unique list of dates to prepopulate the dictionary
unique_dates = list(set([r[0] for r in data_fixed_dates]))
# Create a dictionary embedded within a dictionary to allow for nesting variables
data_dict = {d: {} for d in unique_dates}
# print(data_dict)

# Create a def function that replaces the response string with a single integer
def replace_resp(text, dict):
	for i, j in dict.items():
		text = text.replace(i, j)
	return text

# Dictionary with replacements for each possible response that includes more than just an integer
replace_dict = {"Yes": "1", "No": "0", "a) more than 8 hours": "1", "b) 7-8 hours": "2", "c) 5-6 hours": "3",
				"d) 3-4 hours": "4", "e) 0-2 hours": "5", "5 very poor": "5", "4 poor": "4", "3 fair": "3",
				"2 good": "2", "1 very good": "1", "8 extremely": "8", "6 very much": "6", "4 much": "4",
				"2 somewhat": "2", "0 not at all": "0", "8 the whole time": "8", "6 much": "6",
				"2 a little": "2", "6 very": "6", "4 somewhat": "4", "0 none": "0", "1 1-10min": "1",
				"2 11-20 min": "2", "2 21-30 min": "2", "3 21-30min": "3", "4 31-40min": "4", "5 41-50min": "5",
				"6 51-60min": "6", "7 61-70min": "7", "8 71-80min": "8", "4 some": "4"}

# Loops through each entry with the list data_fixed dates to extract the date (at position [0]) and time (at position [1])
for r in data_fixed_dates:
	date = r[0]
	time = r[1]
    # Check to see if the time is not within the dictionary (that has already been prepopulated with the date)
    # If the time point is not in the dictionary, add it next to the date and prep the dictionary for another nested variable {}
	if time not in data_dict[date]:
		data_dict[date][time] = {}
	# Identify the question ID number within the dataset (at position [3])
	qnum = r[3]
	# Strip punctuation and the quotes around each response
	resp_working = r[-1].replace('"', '').strip()
	# Replace strings with single integers using the def function
	resp = replace_resp(resp_working, replace_dict)
	# If there is no response, replace the blank with the response (empty) instead
	if resp == "":
		resp = "(empty)"
	# Add response as the value in the triple nested dictionary
	data_dict[date][time][qnum] = resp

# Create a list using set that extracts all the unique question IDs
# Recasts the unique question IDs as int to allow the numbers to sort in order from smallest to largest
# These will become the headers for each row
unique_qnums = list(set([int(r[3]) for r in data_fixed_dates]))
unique_qnums.sort()
unique_qnums = [str(i) for i in unique_qnums]

# Create a list that will gather the data for each row for the final .csv file
# Create headers for the dataset
datarows = []
headers = ['date', 'time', 'response_number'] + unique_qnums
# Loop through each date within the dictionary
for date in data_dict.keys():
	# Create a counter that will count each timepoint within a single date
	responsecounter = 1
	# Loop through each time point within the dictionary
	for time in data_dict[date].keys():
		row = [date, time, responsecounter]
		# Create a new variable that contains just the 3 unique variables together: date, time, question ID
		datachunk = data_dict[date][time]
		# Loop through each question ID with the unique question ID set
		for q in unique_qnums: #looping like this maintains a consistant order
			# If the question ID is contained within the variable datachunk, create an entry
			if q in datachunk:
				row.append(datachunk[q])
			# If the question ID is not contained within the datachunk combination, add it and make the response 999
			# This is for branching logic and if questions were not answered within a given time point
			else:
				row.append(999)
		datarows.append(row)
		# Add one to the response counter, which counts the number of questionnaire sets responded to each day
		responsecounter += 1
# print(unique_qnums)

# Create a file output name using the original .txt name
output_name = file_name.replace('.txt', '.csv')

# Write the dataset created with the missing values added to the file output name
with open(output_name, 'w') as fout:
	out = csv.writer(fout)
	out.writerow(headers)
	out.writerows(datarows)
