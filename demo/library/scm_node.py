#!/usr/bin/env python
from ansible.module_utils.basic import *
import requests

def node_present(data):

    user = data['user']
    password = data['password']
    url = data['url']
    org = data['org']
    site = data['site']

    org_id = ''
    site_id = ''
    node_id = ''

    r = requests.get(url+"orgs", auth=(user, password), verify=False).json()
    for n in r['items']:
        if org in n['name']:
            org_id = n['id']

    if org_id == '':
        return(False,True,{"meta": "No such org:"+org})

    r = requests.get(url+"org/"+org_id+"/sites", auth=(user, password), verify=False).json()
    for n in r['items']:
        if site in n['name']:
            site_id = n['id']

    if site_id == '':
        return(False,True,{"meta": "No such site:"+site})

    r = requests.get(url+"org/"+org_id+"/nodes", auth=(user, password), verify=False).json()
    for n in r['items']:
        if n['site'] is None:
            o = requests.delete(url+"node/"+n['id'], auth=(user, password), verify=False)
        elif site_id in n['site']:
            node_id = n['id']
            return (False, False, {"node_id": n['id']})

    payload = {
        "model": data['model'],
        "site": site_id
        }
    r = requests.post(url+"org/"+org_id+"/node/virtual/register", auth=(user, password), json=payload, verify=False).json()
    node_id=r['id']
    return (True, False, {"node_id": r['id']})

def node_absent(data=None):
    user = data['user']
    password = data['password']
    url = data['url']
    org = data['org']
    site = data['site']
    org_id = ''
    site_id = ''
    node_id = ''

    r = requests.get(url+"orgs", auth=(user, password), verify=False).json()
    for n in r['items']:
        if org in n['name']:
            org_id = n['id']

    if org_id == '':
        return(False,True,{"meta": "No such org:"+org})

    r = requests.get(url+"org/"+org_id+"/sites", auth=(user, password), verify=False).json()
    for n in r['items']:
        if site in n['id']:
            site_id = n['id']
            r = requests.delete(url+"site/"+site_id, auth=(user, password), verify=False)

    if site_id == '':
        return(False,True,{"meta": "No such site:"+site})

    r = requests.get(url+"org/"+org_id+"/nodes", auth=(user, password), verify=False).json()
    for n in r['items']:
        if (n['site'] is None) or (site_id in n['site']):
            o = requests.delete(url+"node/"+n['id'], auth=(user, password), verify=False)
            return(True,False,{"meta": "Removed node:"+n['id']})

def main():
    fields = {
        "user": {"required": True, "type": "str"},
        "password": {"required": True, "type": "str", "no_log": True},
        "url": {"required": True, "type": "str" },
        "org": {"required": True, "type": "str"},
        "site": {"required": True, "type": "str"},
        "model": {"required": False, "type": "str", "default": "yogi"},
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
