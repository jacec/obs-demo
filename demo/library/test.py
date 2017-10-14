import requests

user = admin
password = pppp
url = https://proscm.service.rvbdemo.com/api/scm.config/1.0/
org = LOREAL
site = HQ
zone = LAN
node = ''
node_id = ''

org_id = ''
net_segment =''
port_id = ''
zone_id = ''
site_id = ''

r = requests.get(url+"orgs", auth=(user, password), verify=False).json()
for n in r['items']:
    if org in n['name']:
        org_id = n['id']

print org_id
if org_id == '':
    print "no org"
    #return(False,True,{"meta": "No such org:"+org})

r = requests.get(url+"org/"+org_id+"/sites", auth=(user, password), verify=False).json()
for n in r['items']:
    if n['name'] is site:
        site_id = n['id']

if site_id == ''
    print "no site"
    #return(False,True,{"meta": "No network segments"})

r = requests.get(url+"site/"+site_id+"/zones", auth=(user, password), verify=False).json()
for n in r['items']:
    if  n['name'] is zone:
        zone_id = n['id']

if zone == ''
    print "no zone"
    #return(False,True,{"meta": "No network segments"})

r = requests.get(url+"site/"+site_id+"/nodes", auth=(user, password), verify=False).json()
for n in r['items']:
    if  n['serial'] is serial:
        node_id = n['id']

if node_id == ''
    print "no node"
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
