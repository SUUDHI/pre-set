# Find the next greater number , if not present in the list print(-1)
#OUTPUT :[8, 9, 9, 6, 9, 9, -1, 1, -1]
arr = [1,8,7,4,6,3,9,0,1]

for i in range(len(arr)):
    for j in range(i+1,len(arr)):
        if i != j and arr[i] < arr[j]:
            arr[i] = arr[j]
            break
    else:
        arr[i] = -1

print(arr)
