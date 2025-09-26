data = ['apple', 'banana', 'apple', 'orange', 'apple']

freq_table = {}
for item in data:
    if item in freq_table:
        freq_table[item] += 1
    else:
        freq_table[item] = 1

print(freq_table)


