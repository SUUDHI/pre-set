# Reverse Words in a Sentence
#Input: "Hello World from Python"
#Output: "Python from World Hello"
from manual_split import manual_split 

input_sentence  = "Hello World from Python"

splited_input = manual_split(input_sentence)

rev_sentence  = ""

for i in splited_input:
    rev_sentence  = i+ " " + rev_sentence 

print(rev_sentence )
