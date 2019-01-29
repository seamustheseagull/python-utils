import requests
import json
import os
import time

def get_my_ip():

    req = requests.get("https://wtfismyip.com/json")
    #print(req.content)
    data = json.loads(req.text)

    return data["YourFuckingIPAddress"]

def build_headers(credentials):
    return {"X-Auth-Email" : credentials['login_email'],
                "X-Auth-Key" : credentials['api_key'],
                "Content-Type" : "application/json" }

def get_zone_id(api_url, headers, domain):

    url = "%s/zones?name=%s&status=active" % (api_url, domain)

    req = requests.get(url, headers=headers)

    if(req.status_code and req.status_code == 200):
        data = json.loads(req.text)
        return data['result'][0]['id']
    else:
        return None

def get_host_details(api_url, headers, zone_id, hostname):

    details_url = ("%s/zones/%s/dns_records?type=A&name=%s" % (api_url, zone_id, hostname))

    details = requests.get(details_url, headers=headers)

    host_data = {
        "id" : None,
        "current_ip" : None
    }

    if(details.status_code and int(details.status_code < 400)):
        data = json.loads(details.text)
        if(len(data['result'])):
            host_data['id'] = data['result'][0]['id']
            host_data['current_ip'] = data['result'][0]['content']
    
    return host_data

def log_data(logFile, msgtype, message):
    aggregated_message = "%s [%s] %s\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), msgtype.upper(), message)

    with open(logFile, "a+") as log:
        log.write(aggregated_message)

def main():

    source_data = "credentials.json"

    logFile = "refresh_dns.log"

    credential_json = '{ "login_email" : "someone@somewhere.there", "api_key" : "areallylongstringofrandomcharspurplemonkeydishwasher" ,"target_hostname" : "myhost", "target_domain" : "cloudflaremanaged.domain" }'

    log_data(logFile, "Info", "Running IP Address Update")

    if os.path.exists(source_data):
        with open(source_data, 'r') as cred_file:
            credential_json = cred_file.read()
    else:
        log_data(logFile, "Error", "Could not locate config file @ '%s'" % source_data)
    
    credentials = json.loads(credential_json)
    
    headers = build_headers(credentials)
    
    endpoint = "https://api.cloudflare.com/client/v4/"

    zone_identifier = get_zone_id(endpoint, headers, credentials['target_domain'])

    host_details = get_host_details(endpoint, headers, zone_identifier, ("%s.%s" % (credentials['target_hostname'], credentials['target_domain'])))
    
    log_data(logFile, "Debug", "My Info - Host: '%s'; Domain: '%s'" % (credentials['target_hostname'], credentials['target_domain']))

    if(host_details['id'] != None):

        new_ip = get_my_ip()

        if(new_ip and host_details['current_ip'] != new_ip):
            
            update_url = ("%s/zones/%s/dns_records/%s" % (endpoint, zone_identifier, host_details['id']))
                      
            log_data(logFile, "Info", "My IP has changed. Updating my IP to %s; IP in DNS record: %s" % (new_ip, host_details['current_ip']))
            payload = {
                        "type" : "A",
                        "name" : ("%s.%s" % (credentials['target_hostname'], credentials['target_domain'])),
                        "content" : new_ip
                        }

            req = requests.put(update_url, data=json.dumps(payload), headers=headers)


            if(req.status_code and req.status_code == 200):
                log_data(logFile, "Info", "IP successfully updated")
            else:
                log_data(logFile, "Error", "Something went wrong with the update: %s" % (req.text))

        elif(new_ip == host_details['current_ip']):
            log_data(logFile, "Info", "IP does not require update. My IP: %s; IP in DNS record: %s" % (new_ip, host_details['current_ip']))
        else:
            log_data(logFile, "Error", "Could not obtain my IP address from external source. No update performed")

if __name__ == "__main__":
    main()
