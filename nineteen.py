my_dict = {'a': 10, 'b': 25, 'c': 15, 'd': 30, 'e': 20}
max_key = None
max_value = 0
for key, value in my_dict.items():
    if value > max_value:
        max_value = value
        max_key = key

print("Key with maximum value:", max_key)
print("Maximum value:", max_value)