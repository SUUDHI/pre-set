def Anagrams(input_1,input_2):
    input_1.lower()
    input_2.lower()

    input_1 = sorted(input_1)
    input_2 = sorted(input_2)

    if input_1 == input_2:
        print("strings are anagrams")
    else:
        print("strings are non anagrams ")
    
input_1 = 'slient'
input_2 = 'listen'

Anagrams(input_1,input_2)
