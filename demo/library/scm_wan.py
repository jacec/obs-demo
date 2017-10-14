#!/usr/bin/env python
from ansible.module_utils.basic import *
import requests

def node_present(data):

    user = data['user']
    password = data['password']
    url = data['url']
    org = data['org']
    wan = data['wan']

    org_id = ''
    wan_id = ''

    r = requests.get(url+"orgs", auth=(user, password), verify=False).json()
    for n in r['items']:
        if org in n['name']:
            org_id = n['id']

    if org_id == '':
        return(False,True,{"meta": "No such org:"+org})

    r = requests.get(url+"org/"+org_id+"/wans", auth=(user, password), verify=False).json()
    for n in r['items']:
        if wan in n['name']:
            wan_id = n['id']
            return (False, False, {"wan_id": n['id']})

    payload = {
        "name": data['wan'],
        "longname": data['wan_long'],
        "internet": data['internet']
        }
    r = requests.post(url+"org/"+org_id+"/wans", auth=(user, password), json=payload, verify=False).json()
    wan_id=r['id']
    return (True, False, {"wan_id": wan_id})

def node_absent(data=None):
    user = data['user']
    password = data['password']
    url = data['url']
    org = data['org']
    org_id = ''
    wan_id = ''

    r = requests.get(url+"orgs", auth=(user, password), verify=False).json()
    for n in r['items']:
        if org in n['name']:
            org_id = n['id']

    if org_id == '':
        return(False,True,{"meta": "No such org:"+org})

    r = requests.get(url+"org/"+org_id+"/wans", auth=(user, password), verify=False).json()
    for n in r['items']:
        if n['name'] is data['wan']:
            o = requests.delete(url+"wan/"+n['id'], auth=(user, password), verify=False)
            return(True,False,{"wan": data['wan']})

def main():
    fields = {
        "user": {"required": True, "type": "str"},
        "password": {"required": True, "type": "str", "no_log": True},
        "url": {"required": True, "type": "str" },
        "org": {"required": True, "type": "str"},
        "wan": {"required": True, "type": "str"},
        "wan_long": {"required": True, "type": "str"},
        "internet": {"required": False, "type": "str", "default": "true"},
        "state": {
            "default": "present",
            "choices": ['present', 'absent'],
            "type": 'str'
        },
    }

    choice_map = {
      "present": node_present,
      "absent": node_absent,
    }

    module = AnsibleModule(argument_spec=fields)
    has_changed, has_failed, result = choice_map.get(module.params['state'])(module.params)
    module.exit_json(changed=has_changed, failed=has_failed, meta=result)

if __name__ == '__main__':
    main()
