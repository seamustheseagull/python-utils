import sys
import json

input_file = sys.argv[1]

output_file = ("%s/addresses.csv" % sys.path[0])

open(output_file, 'w').close()

with open(input_file, 'r') as inf:
    data = inf.read()

addresses = json.loads(data)

with open(output_file, 'a') as out_file:
    for address in addresses:
        line = ("%s|%s|%s|%s\n" % (address['rollnum'], address['lat'], address['lng'], address['map_code']))
        out_file.write(line)
