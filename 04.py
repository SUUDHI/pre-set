test_dict = {"a" : 4, "b" : 4, "c" : 4, "d" : 4, "e" : 4}

mean_num = len(test_dict)

val_total = 0

for key, value in test_dict.items():
    val_total += value

print(val_total/mean_num) 
