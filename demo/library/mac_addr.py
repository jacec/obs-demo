#!/usr/bin/python
# macgen.py script to generate a MAC address for guests on Xen
#
import random
import json
#

def randomMAC():
    mac= [ 0x00, 0x16, 0x3e,
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff) ]
    return ':'.join(map(lambda x: "%02x" % x, mac))

if __name__ == '__main__':
    output={}
    output.update(changed=True)
    output.update(mac=randomMAC())
    json_string=json.dumps(output)
    print( json_string )
