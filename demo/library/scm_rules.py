#!/usr/bin/env python
from ansible.module_utils.basic import *
import requests

def rules_present(data):

    user = data['user']
    password = data['password']
    url = data['url']
    org = data['org']
    direction = data['direction']

    org_id = ''
    network_segments = []

    r = requests.get(url+"orgs", auth=(user, password)).json()
    for n in r['items']:
        if org in n['name']:
            org_id = n['id']

    if org_id == '':
        return(False,True,{"meta": "No such org:"+org})

    r = requests.get(url+"org/"+org_id+"/networks", auth=(user, password)).json()
    for n in r['items']:
        if not n['zone'] is None:
            network_segments.append(n['zone'])

    if network_segments == []:
        return(False,True,{"meta": "No network segments"})

    payload = {
        "dsttype": "any",
        "active": "1",
        "srctype": "segments",
        "source_zones": network_segments,
        "allow": "1"
        }

    r = requests.get(url+"org/"+org_id+"/"+direction+"_rules", auth=(user, password)).json()
    for n in r['items']:
        if 'segments' in n['srctype']:
            o = requests.put(url+"org/"+org_id+"/"+direction+"_rules", auth=(user, password), json=payload).json()
            return (True, False, {"network_segments updated": network_segments, "response": o})
        else:
            o = requests.post(url+"org/"+org_id+"/"+direction+"_rules", auth=(user, password), json=payload).json()
            return (True, False, {"network_segments created": network_segments, "response": o, "payload": payload})

def rules_absent(data=None):
    user = data['user']
    password = data['password']
    url = data['url']
    org = data['org']
    direction = data['direction']
    org_id = ''
    rule_id = ''

    r = requests.get(url+"orgs", auth=(user, password)).json()
    for n in r['items']:
        if org in n['name']:
            org_id = n['id']

    if org_id == '':
        return(False,True,{"meta": "No such org:"+org})

    r = requests.get(url+"org/"+org_id+"/"+direction+"_rules", auth=(user, password)).json()
    for n in r['items']:
        if 'segments' in n['srctype']:
            rule_id = n['id']
            r = requests.delete(url+"/"+direction+"_rules/"+rule_id, auth=(user, password))
            return(True,False,{"meta": "Removed rule: "+rule_id})
    if rule_id == '':
        return(False,True,{"meta": "No such rule"})

def main():
    fields = {
        "user": {"required": True, "type": "str"},
        "password": {"required": True, "type": "str", "no_log": True},
        "url": {"required": True, "type": "str" },
        "org": {"required": True, "type": "str"},
        "direction": {"required": False, "type": "str", "default": "outbound"},
        "state": {
            "default": "present",
            "choices": ['present', 'absent'],
            "type": 'str'
        },
    }

    choice_map = {
      "present": rules_present,
      "absent": rules_absent,
    }

    module = AnsibleModule(argument_spec=fields)
    has_changed, has_failed, result = choice_map.get(module.params['state'])(module.params)
    module.exit_json(changed=has_changed, failed=has_failed, meta=result)

if __name__ == '__main__':
    main()
