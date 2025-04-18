lst = [x for x in range(1,21)]

print(lst)

even_list = list(filter(lambda x: x % 2 == 0, lst))

print(even_list)
