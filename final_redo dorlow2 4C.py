# First import sample_palm_data.txt into regular python

infile = open("sample_palm_data.txt", "r")
sample_data = infile.readlines()
infile.close()

print(sample_data)

# Loop through the first instance of each line and split time and date
# Keep timestamp [split, first and second instance], id [third instance], question id [fourth instance], response [final instance]
#
working_data = []
for instance in sample_data:
    stamp = instance[0:15]
    # print(stamp)
    date = int(stamp[0:8])
    time = int(stamp[8:15].rstrip())
    # id = timestamp[21:25].rstrip()  LEAVE ID ALONE FOR NOW
    question_id = int(instance[30:35].strip( ))
    response_quotes = instance[73:].rstrip()
    response = response_quotes.strip('"').rstrip()
    joined_data = [date] + [time] + [question_id] + [response]
    working_data.append(joined_data)
print(working_data)

# Loop through the rows and construct a dictionary-- no need to prepopulate
# pda_dictionary = {}
#
# for row in working_data:
#     current_level = pda_dictionary
#     for section in row:
#         if section not in current_level:
#             current_level[section] = {}
#         current_level = current_level[section]
# print(pda_dictionary)

#prepopulate the dictionary with unique dates
pda_dictionary = {}

# grabs duplicate keys
# for instance in working_data:
#     if instance[0] not in pda_dictionary:
#         pda_dictionary[instance[0]] = [instance[1]]
#     else:
#         pda_dictionary[instance[0]].append(instance[1])

# doesn't grab multiple keys
# for instance in working_data:
#     if instance[0] not in pda_dictionary:
#         pda_dictionary[instance[0]] = [instance[1]]

print(pda_dictionary)


# creating variable for all unique question ids to use as headers
qid_list = []
for qid in working_data:
    qid_list.append(qid[2])
unique_qid = sorted(set(qid_list))
print(unique_qid)

