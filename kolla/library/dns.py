#!/usr/bin/env python
from ansible.module_utils.basic import *
import requests

url=https://api.dnsimple.com/v2
token=NGVlbknnNfjYw33P0M9VV3KifKRrW4xp
header = {'Authorization: Bearer '+token,
          'Accept': 'application/json', 
          'Content-Type': 'application/json' 
         }
