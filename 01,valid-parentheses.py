#Input: s = "()[]{}"

#Output: true
s = "()[]{}"

def is_valid_Parentheses(str):
    Parentheses_dict = {
        ")" : "(",
        "]" : "[",
        "}" : "{"
        }

    stack = []

    for char in str:
        if char in Parentheses_dict:
            if stack and stack[-1] == Parentheses_dict[char]:
                stack.pop()
            else:
                return False
        else:
            stack.append(char)
    
    return True if not stack else False

print(is_valid_Parentheses(s))

# Using if, and, or and ord()
def isValid(s):
    arr = list(str(s))
    stack = []

    if len(arr) % 2 == 1:
        return False

    if arr[0] == '}' or arr[0] == ']' or arr[0] == ')':
        return False

    for char in arr:
        if char == '{' or char == '[' or char == '(':
            stack.append(char)
        elif len(stack) == 0:
            return False
        elif ord(stack[-1]) == ord(char) - 2 or ord(stack[-1]) == ord(char) - 1:
            stack.pop()
        else:
            return False
        #print(stack)

    if len(stack) == 0:
        return True
    else:
        return False
    
print(isValid(s))

