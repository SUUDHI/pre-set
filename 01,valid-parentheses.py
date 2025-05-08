#Input: s = "()[]{}"

#Output: true
s = "()[]{}"

def is_valid_Parentheses(str):
    p_dict = {
        ")" : "(",
        "]" : "[",
        "}" : "{"
        }

    stack = []

    for char in str:
        if char in p_dict:
            if stack and stack[-1] == p_dict[char]:
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

    for i in arr:
        if i == '{' or i == '[' or i == '(':
            stack.append(i)
        elif len(stack) == 0:
            return False
        elif ord(stack[-1]) == ord(i) - 2 or ord(stack[-1]) == ord(i) - 1:
            stack.pop()
        else:
            return False
        #print(stack)

    if len(stack) == 0:
        return True
    else:
        return False
    
print(isValid(s))

