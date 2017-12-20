# 452_finalproject
A project transforming PDA output into an entry-ready dataset.


Documents
Python code: final dorlow2 4C.py
Sample data: sample_palm_data.txt
Questions and palm programming in readable word document: opioidPDA_questions and settings.docx
Programming text file: opioidPDA_questions.txt
How to read palm output: palm_how to read output.pdf

First attempt coding in PyCharm using pandas: final dorlow2 4C.py
Second attempt at coding in Jupyter Notebook using pandas: FinalProject452.ipynb
Third attempt at coding PyCharm using pure python: final_redo dorlow2 4C.py 

Modification of code by Elizabeth Wickes: 452 final dorlow2 4C.py 
Code modification includes a def replace_resp() function that uses a dictionary to replace string responses with numbers, and an
additional variable that keeps the input name but changes the extension from .txt to .csv
Supplemental documentas created by this file: sample_palm_dataTEMP.csv, sample_palm_data.csv

Goals
a.	Extract the participant ID, located in column 7
b.	Extract the first half of the timestamp in column 1, consisting of YYYYMMDD, in the format MM/DD/YYYY
c.	Extract he second half of the timestamp in column 1, consisting of HHMMSS, in the format HH:MM:SS
d.	Extract the question ID in column 8; if it is -32767 this means that the question was never answered and should be represented by the number 999*
e.	Extract the response time in column 9, consisting of 1/100 seconds, in the format x.xx
f.	Extract the response in column 10, consisting of numbers that correspond to the order of the response choice within a presented range
    1= not at all, 2= a little, 3=somewhat, 4=very much, 5=completely [Selecting “very much” would be represented by a “4”]

g. If the question was never answered, I still want Python print all the question IDs, with the number 999 listed as the values
h.	*There is a little bit of branching logic in the palm pilot programming. I still want Python to print the skipped questions with the number 999 listed as the values
    i.	If they answered “yes” to the first entry of the day, they are prompted to answer two questions about duration and quality of sleep. Else, this was skipped.
    ii.	If they responded a 2 (somewhat) or more for questions about being irritated or annoyed, they receive an additional 4 questions. Else, this was skipped.
