#!/usr/bin/env python
from ansible.module_utils.basic import *
import requests
import time

def image_present(data):

    user = data['user']
    password = data['password']
    url = data['url']
    org = data['org']
    site = data['site']

    org_id = ''
    site_id = ''
    image_id = ''
    timer=0

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

    payload = {"type": data['type']}
    r = requests.post(url+"node/"+node_id+"/prepare_image", auth=(user, password), json=payload, verify=False).json()

    while True:
        r = requests.get(url+"node/"+node_id+"/image_status", auth=(user, password), verify=False)
        if r.status_code == requests.codes.ok:
            r = requests.get(url+"node/"+node_id+"/image_status", auth=(user, password), verify=False).json()
            return (True, False, url+"node/"+node_id+"/get_image?file="+r['image_file'])
        time.sleep(1)
        timer += 1
        if timer >= data['timeout']:
            break

    return (False,True,{"meta": "timeout reached without image completion"})

def main():
    fields = {
        "user": {"required": True, "type": "str"},
        "password": {"required": True, "type": "str", "no_log": True},
        "url": {"required": True, "type": "str" },
        "org": {"required": True, "type": "str"},
        "site": {"required": True, "type": "str"},
        "type": {"required": False, "type": "str", "default": "kvm"},
        "timeout": {"required": False, "type": "str", "default": "120"},
        "state": {
            "default": "present",
            "choices": ['present', 'absent'],
            "type": 'str'
        },
    }

    # choice_map = {
    #   "present": image_present,
    #   "absent": image_absent,
    # }

    module = AnsibleModule(argument_spec=fields)
    has_changed, has_failed, result = image_present(module.params)
    module.exit_json(changed=has_changed, failed=has_failed, image=result)

if __name__ == '__main__':
    main()
