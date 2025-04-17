"""
Palindrome Checker:
Write a function that checks if a given string is a palindrome (reads the same forwards and backwards)."""

def palindrome(string):
    rev_str = string[: : -1]
    
    if string == rev_str:
        print(f"{rev_str} is a palindrome")
    else:
        print(f"{string} is non palindrome")

s1 = input("Enter a string: ")
palindrome(s1)
