from os import listdir
from os.path import join, isfile
import eletility

path = "../Output/vis"
files = [f for f in listdir(path) if isfile(join(path, f))]

files.sort()

handler = eletility.Files()

processed = []
node_name = 'a'
max_found_length = 0

prev_lines = None
for file in files:
    processed_file = []
    with open(join(path, file), "r") as f:
        lines = f.readlines()
        if lines == prev_lines:
            continue
        else:
            prev_lines = lines
        if len(lines) > max_found_length:
            max_found_length = len(lines)
        for line in lines:
            x, y = line.strip().split(",")
            x, y = int(x), int(y)
            if x <= 0 <= y:
                loc = 1
            elif x >= 0 and y >= 0:
                loc = 2
            elif x <= 0 and y <= 0:
                loc = 3
            elif y <= 0 <= x:
                loc = 4
            processed_file.append((node_name, loc))
            node_name = chr(ord(node_name) + 1)
    node_name = "a"
    processed.append(processed_file)
    # print(processed_file)

connections = ""
base = "a"
for i in range(max_found_length):
    for j in range(max_found_length):
        if i == j:
            continue
        connections += chr(ord(node_name) + i) + "," + chr(ord(node_name) + j) + "\n"
handler.writeTruncate("connections.txt", connections)

similarities = {}
key = "a"

for i in range(max_found_length):
    similarities[key] = []
    key = chr(ord(key) + 1)

base = "a"
for data in processed:
    for i in range(max_found_length):
        if len(data) - 1 < i:
            similarities[chr(ord(base) + i)].append("")
            continue
        similarities[data[i][0]].append(data[i][1])

sim_contents = "Time,"
for i in range(len(similarities[list(similarities.keys())[0]])):
    sim_contents += "c" + str(i) + ","

sim_contents = sim_contents[:-1] + "\n"

for key in similarities:
    sim_contents += key + ","
    for value in similarities[key]:
        sim_contents += str(value) + ","
    sim_contents = sim_contents[:-1] + "\n"

handler.writeTruncate("similarities.csv", sim_contents)
