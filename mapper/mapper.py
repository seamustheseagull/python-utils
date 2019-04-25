import requests
import json
import sys

key = "AIzaSyDSPoVotHJfKYf8iJxkXwQ9e_CBLYN3bAI"

base_url = "https://maps.googleapis.com/maps/api/geocode/json?"

my_context = sys.path[0]

out_file = ("%s/address_list.json" % my_context)
raw_out_file = ("%s/raw_data.json" % my_context)

open(out_file, 'w').close()
open(raw_out_file, 'w').close()

in_file = sys.argv[1]

with open(in_file, "r", encoding="utf-8") as f: 
    address_list = f.readlines()
    
out_addresses = list()

i = 1

if(len(address_list)):
    for line in address_list:
        line = line.strip()     
        rollcode, address = line.split("|")   
        full_url = ("%saddress=%s&key=%s" % (base_url, address, key))
        print("%d: %s" % (i, full_url))
        i += 1

        details = requests.get(full_url)

        if(details.status_code and int(details.status_code < 400)):
            data = json.loads(details.text)
            global_code = "ZZZ"
            address_dict = { "rollnum" : rollcode, "address": address, 
                                "lat" : "999", 
                                "lng" : "999",
                                "map_code" : global_code
                            }
            if "results" in data:
                if(data['status'] != "ZERO_RESULTS"):
                    if "plus_code" in data['results'][0]:
                        global_code = data['results'][0]['plus_code']['global_code']
                    address_dict = { "rollnum" : rollcode, "address": address, 
                                "lat" : data['results'][0]['geometry']['location']['lat'], 
                                "lng" : data['results'][0]['geometry']['location']['lng'],
                                "map_code" : global_code
                            }

            with open(raw_out_file, "a+") as fo:
                json.dump(data, fo)
                fo.write(",")

        else:
            address_dict = { "rollnum" : rollcode, "address": address, 
                        "lat" : "999", 
                        "lng" : "999",
                        "map_code" : "XXX"
                    }

        with open(out_file, 'a+') as outfile:
            json.dump(address_dict, outfile)
            outfile.write(",")
        #out_addresses.append(address_dict)



#print(json.dumps(out_addresses))

