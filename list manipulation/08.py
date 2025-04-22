# Count Strings with Same Start and End

data = ['abc', 'xyz', 'aba', '1221']

count = 0

for word in data:
    if len(word) > 1 and word[0] == word[-1]:
        count += 1

print(count)