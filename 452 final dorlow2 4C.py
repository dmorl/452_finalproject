## Convert it all to a CSV for pure python

import pandas as pd

file_name = 'sample_palm_data.txt'
palm_data = pd.read_fwf(file_name, header=None)


palm_data.columns = ["Time", "PDA ID", "Question ID", "Time to Respond*", "Answer ID", "Question Type",
					 "Question Set ID", "Response"]
# cols
# ["Time", "PDA ID", "Question ID", "Time to Respond*",
#  "Answer ID", "Question Type", "Question Set ID", "Response"]

palm_data.to_csv('palm_data.csv', index = False)


## now do stuff

import csv

with open('palm_data.csv', 'r') as fin:
	io = csv.reader(fin)
	headers = next(io)
	data = [r for r in io]

data_fixed_dates = []

# split out the date and time
for row in data:
	date = row[0][:8]
	time = row[0][8:]
	data_fixed_dates.append([date, time] + row[1:])

unique_dates = list(set([r[0] for r in data_fixed_dates]))

data_dict = {d: {} for d in unique_dates}
# print(data_dict)

def replace_resp(text, dict):
	for i, j in dict.items():
		text = text.replace(i, j)
	return text

replace_dict = {"Yes": "1", "No": "0", "a) more than 8 hours": "1", "b) 7-8 hours": "2", "c) 5-6 hours": "3",
				"d) 3-4 hours": "4", "e) 0-2 hours": "5", "5 very poor": "5", "4 poor": "4", "3 fair": "3",
				"2 good": "2", "1 very good": "1", "8 extremely": "8", "6 very much": "6", "4 much": "4",
				"2 somewhat": "2", "0 not at all": "0", "8 the whole time": "8", "6 much": "6",
				"2 a little": "2", "6 very": "6", "4 somewhat": "4", "0 none": "0", "1 1-10min": "1",
				"2 11-20 min": "2", "2 21-30 min": "2", "3 21-30min": "3", "4 31-40min": "4", "5 41-50min": "5",
				"6 51-60min": "6", "7 61-70min": "7", "8 71-80min": "8", "4 some": "4"}

for r in data_fixed_dates:
	date = r[0]
	time = r[1]
	if time not in data_dict[date]:
		data_dict[date][time] = {}
	qnum = r[3]
	resp_working = r[-1].replace('"', '').strip()
	resp = replace_resp(resp_working, replace_dict)
	if resp == "":
		resp = "(empty)"
	data_dict[date][time][qnum] = resp

# recasting to int so the numbers sort correctly
unique_qnums = list(set([int(r[3]) for r in data_fixed_dates]))
unique_qnums.sort()
unique_qnums = [str(i) for i in unique_qnums]

datarows = []
headers = ['date', 'time', 'response_number'] + unique_qnums
for date in data_dict.keys():
	responsecounter = 1
	for time in data_dict[date].keys():
		row = [date, time, responsecounter]
		datachunk = data_dict[date][time]	
		for q in unique_qnums: #looping like this mainians a consistant order
			if q in datachunk:
				row.append(datachunk[q])
			else:
				row.append(999)
		datarows.append(row)
		responsecounter += 1

# print(unique_qnums)

output_name = file_name.replace('.txt', '.csv')

with open(output_name, 'w') as fout:
	out = csv.writer(fout)
	out.writerow(headers)
	out.writerows(datarows)

