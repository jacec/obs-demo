#!/usr/bin/env python
from ansible.module_utils.basic import *
import requests

def org_present(data):

    user = data['user']
    password = data['password']
    url = data['url']
    org = data['org']
    org_id = None

    payload = {
        "name": data['org'],
        "city": data['city'],
        "longname": data['org'],
        "country": data['country'],
        "timezone": data['tz'],
        "sitelink_pool_v4": data['v4pool']
        }

    r = requests.get(url+"orgs", auth=(user, password)).json()
    for n in r['items']:
        if org in n['id']:
            org_id = n['id']
            has_changed = False
        else:
            o = requests.post(url+"orgs", auth=(user, password), json=payload).json()
            org_id = o
            has_changed = True

    meta = {"org_id": org_id, "payload": payload}
    return (has_changed, org_id, meta)

def org_absent(data=None):
    user = data['user']
    password = data['password']
    url = data['url']
    org = data['org']
    org_id = None

    r = requests.get(url+"orgs", auth=(user, password)).json()
    for n in r['items']:
        if org in n['id']:
            org_id = n['id']
            r = requests.delete(url+"org/"+org_id, auth=(user, password)).json()
            has_changed = True
        else:
            r = "none"
            has_changed = False
    meta = {"response": r}
    return (has_changed, None, meta)

def main():
    fields = {
        "user": {"required": True, "type": "str"},
        "password": {"required": True, "type": "str"},
        "url": {"required": True, "type": "str" },
        "org": {"required": True, "type": "str"},
        "city": {"required": True, "type": "str"},
        "country": {"default": "US", "required": False, "type": "str"},
        "tz": {"default": "Americas/Los_Angeles", "required": False, "type": "str"},
        "v4pool": {"default": "172.16.0.0/12", "required": False, "type": "str"},
        "state": {
            "default": "present",
            "choices": ['present', 'absent'],
            "type": 'str'
        },
    }

    choice_map = {
      "present": org_present,
      "absent": org_absent,
    }

    module = AnsibleModule(argument_spec=fields)
    has_changed, org_id, result = choice_map.get(module.params['state'])(module.params)
    module.exit_json(changed=has_changed, org_id=org_id, meta=result)

if __name__ == '__main__':
    main()
