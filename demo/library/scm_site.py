#!/usr/bin/env python
from ansible.module_utils.basic import *
import requests

def site_present(data):

    user = data['user']
    password = data['password']
    url = data['url']
    org = data['org']

    payload = {
        "name": data['site'],
        "city": data['city'],
        "longname": data['site'],
        "country": data['country'],
        "timezone": data['tz'],
        "dnsroutes": "@20.20.1.2"
        }

    org_id = ''

    r = requests.get(url+"orgs", auth=(user, password)).json()
    for n in r['items']:
        if org in n['name']:
            org_id = n['id']

    if org_id == '':
        return(False,True,r)

    r = requests.get(url+"org/"+org_id+"/sites", auth=(user, password)).json()
    for n in r['items']:
        if data['site'] in n['name']:
            return(False,False,{"site_id": n['id']})
    else:
        r = requests.post(url+"org/"+org_id+"/sites", auth=(user, password), json=payload).json()
        return (True, False, {"site_id": r['id']})

def site_absent(data=None):
    user = data['user']
    password = data['password']
    url = data['url']
    org = data['org']
    site = data['site']
    org_id = ''
    site_id = ''

    r = requests.get(url+"orgs", auth=(user, password)).json()
    for n in r['items']:
        if org in n['name']:
            org_id = n['id']

    if org_id == '':
        return(False,True,r)

    r = requests.get(url+"org/"+org_id+"/sites", auth=(user, password)).json()
    for n in r['items']:
        if site in n['id']:
            site_id = n['id']
            r = requests.delete(url+"site/"+site_id, auth=(user, password))

    if site_id == '':
        return(False,False,{"site": "non-existent"})

    return (True, False, {"site_id": site_id})

def main():
    fields = {
        "user": {"required": True, "type": "str"},
        "password": {"required": True, "type": "str", "no_log": True},
        "url": {"required": True, "type": "str" },
        "org": {"required": True, "type": "str"},
        "site": {"required": True, "type": "str"},
        "city": {"required": True, "type": "str"},
        "country": {"default": "US", "required": False, "type": "str"},
        "tz": {"default": "Americas/Los_Angeles", "required": False, "type": "str"},
        "state": {
            "default": "present",
            "choices": ['present', 'absent'],
            "type": 'str'
        },
    }

    choice_map = {
      "present": site_present,
      "absent": site_absent,
    }

    module = AnsibleModule(argument_spec=fields)
    has_changed, has_failed, result = choice_map.get(module.params['state'])(module.params)
    module.exit_json(changed=has_changed, failed=has_failed, meta=result)

if __name__ == '__main__':
    main()
