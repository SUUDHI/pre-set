# Reverse Words in a Sentence
#Input: "Hello World from Python"
#Output: "Python from World Hello"

input_sentence  = "Hello World from Python"

splited_input = input_sentence .split()

rev_input = splited_input[::-1]

print(rev_input)

rev_sentence  = ""

#with using loop
for i in splited_input:
    rev_sentence  = i+ " " + rev_sentence 

print(rev_sentence )
