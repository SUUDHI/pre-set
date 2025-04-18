"""
Palindrome Checker:
Write a function that checks if a given string is a palindrome (reads the same forwards and backwards)."""

def palindrome(string):
    reversed_string = ""

    for char in string:
        reversed_string = char + reversed_string
    
    if string == reversed_string:
        print(string,"is an Palindrome.")
    else:
        print(string,"not an palindrome.")

string_check = input("Enter a string to check: ")

palindrome(string_check)