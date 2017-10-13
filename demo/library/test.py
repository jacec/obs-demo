import requests

user = admin
password = pppp
url = https://proscm.service.rvbdemo.com/api/scm.config/1.0/
org = data['org']
direction = data['direction']

org_id = ''
network_segments = []

r = requests.get(url+"orgs", auth=(user, password), verify=False).json()
for n in r['items']:
    if org in n['name']:
        org_id = n['id']

print org_id
if org_id == '':
    print "no org"
    #return(False,True,{"meta": "No such org:"+org})

r = requests.get(url+"org/"+org_id+"/networks", auth=(user, password), verify=False).json()
for n in r['items']:
    if not n['zone'] is None:
        network_segments.append(n['zone'])

if network_segments == []:
    print "no network segments"
    #return(False,True,{"meta": "No network segments"})

payload = {
    "dsttype": "any",
    "active": "1",
    "srctype": "segments",
    "source_zones": network_segments,
    "allow": "1"
    }

r = requests.get(url+"org/"+org_id+"/"+direction+"_rules", auth=(user, password), verify=False).json()
for n in r['items']:
    if 'segments' in n['srctype']:
        o = requests.put(url+"org/"+org_id+"/"+direction+"_rules", auth=(user, password), json=payload, verify=False).json()
        return (True, False, {"network_segments updated": network_segments, "response": o, "payload": payload})
    else:
        o = requests.post(url+"org/"+org_id+"/"+direction+"_rules", auth=(user, password), json=payload, verify=False).json()
        return (True, False, {"network_segments created": network_segments, "response": o, "payload": payload})
