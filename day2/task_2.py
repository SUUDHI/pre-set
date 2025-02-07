"""
Write a program that:
Takes a sentence as input.
Prints:
The sentence in uppercase.
The total number of words in the sentence.
The sentence in reverse order.
Example Output:
Enter a sentence: Python is fun  

Uppercase: PYTHON IS FUN  
Number of words: 3  
Reversed sentence: fun is Python  
"""
sentence = input("enter sentence: ")

print(sentence)
print("")

print(sentence.upper()) #convert this into a uper case string
print("")


ns = sentence.split()
print(ns)

ns.reverse()
print(ns)

suu=' '.join(ns)
print(suu)



