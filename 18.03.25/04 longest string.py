# Given a string, find the length of the longest substring without repeating characters.

s = "abcadcbb"
d = []
for i in s:
    if i not in d:
        d.append(i)

print("".join(d))
# i know a loop hole in this approch like what if the longest sub string in in the middle.
