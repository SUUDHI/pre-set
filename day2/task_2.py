sentence = input("enter sentence: ")

print(sentence.upper()) #convert this into a uper case string
#counting words
word_count = len(sentence.split())
counter=sentence.count(" ")
counter+=1
print(counter)

#reverse a string
reverse_sentence = sentence.split()
reverse_sentence.reverse()
join_again=' '.join(reverse_sentence)
print(f"Reversed string : {join_again}")
