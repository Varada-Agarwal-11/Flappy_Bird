# Read the data from the file
with open('flappy_bird_data.txt', 'r') as file:
    lines = file.readlines()

# Process the data to keep the first '1)' in each data set of consecutive '1)' and replace the rest with '0)'
processed_lines = []
found_first_one = False

for line in lines:
    if '0)' in line:
        found_first_one = False

    if '1)' in line:
        if found_first_one:
            line = line.replace('1)', '0)')
        else:
            found_first_one = True

    processed_lines.append(line)

# Write the processed data back to the file
with open('flappy_bird_data_processed.txt', 'w') as file:
    file.writelines(processed_lines)
