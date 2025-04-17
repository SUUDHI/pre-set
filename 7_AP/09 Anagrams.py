def Anagrams(st1,st2):
    st1.lower()
    st2.lower()

    st1 = sorted(st1)
    st2 = sorted(st2)

    if st1 == st2:
        print("strings are anagrams")
    else:
        print("strings are non anagrams ")
    
   
s1 = 'slient'
s2 = 'listen'

Anagrams(s1,s2)