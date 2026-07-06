my_list = [1, 2, 3, 2, 4, 1, 5, 3, 6]
unique_list = []
for item in my_list:
    if item not in unique_list:
        unique_list.append(item)
        
print("Original list:", my_list)
print("After removing duplicates:", unique_list)