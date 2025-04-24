# Maximum Number of Words Found in Sentences

sentences = ["alice and bob love leetcode", "i think so too", "this is great thanks very much"]

len_sentences = []

max_sentences = []

for i in sentences:
    len_sentences.append(len(i))

print(len_sentences)

max = 0

for item in range(len(len_sentences)):
    if len_sentences[item] > max:
        max = len_sentences[item]

print(max)

for item in range(len(len_sentences)):
    if len_sentences[item] == max:
        max_sentences.append(sentences[item])

print(max_sentences)
