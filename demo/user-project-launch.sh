#!/bin/bash

. ~/open.rc

set -ex
# Create project
openstack project create obs
# Create user
openstack user create obs --project obs --password obs
# Associate user with project
openstack role add --user obs --project obs _member_
# Create flavor
openstack  flavor create --id 100 --ram 32768 --disk 120 --vcpus 16 --project obs --private  obs.base

# Create network and security group information

openstack  network create obs --project obs
openstack  subnet create obs --subnet-range 192.168.100.0/24 --project obs --dns-nameserver 53.255.82.245 --dns-nameserver 53.255.64.245 --dhcp --network obs 


openstack  router create mos-router --project obs --ha 

openstack  router set mos-router --external-gateway public 
openstack  router add subnet mos-router obs 

# Adjust the default security group.  This is not good practice
default_group=`openstack  security group list --project obs  | awk '/ default / {print $2}'`
openstack  security group rule create --ingress --dst-port 22 --protocol tcp --remote-ip 0.0.0.0/0 ${default_group}  
openstack  security group rule create --ingress --dst-port 80 --protocol tcp --remote-ip 0.0.0.0/0 ${default_group}  
openstack  security group rule create --ingress --dst-port 443 --protocol tcp --remote-ip 0.0.0.0/0 ${default_group}  
openstack  security group rule create --ingress --protocol icmp --remote-ip 0.0.0.0/0 ${default_group}  

# Change to obs user
export OS_PROJECT_NAME="obs"
export OS_USERNAME="obs"
export OS_PASSWORD=obs
# Add ssh key
if [[ "$(openstack keypair list -c Name --quote none -f value | grep id_rsa)" != "id_rsa" ]] ; then
echo adding keypair
openstack  keypair create --public-key ~/.ssh/id_rsa.pub id_rsa
fi

# Get our needed image
if [ ! -f trusty.img ]; then
curl https://cloud-images.ubuntu.com/trusty/current/trusty-server-cloudimg-amd64-disk1.img > trusty.img
fi
openstack  image create --container-format bare --disk-format qcow2 --min-disk 2 --min-ram 1000 --public --file trusty.img trusty

#Launch VM with cloud-init script
echo adding server
openstack  server create --flavor obs.base --image trusty --nic net-id=obs --key-name id_rsa obs --user-data obs_init

# Get Floating IP
echo grabbing a floating IP
floating_ip=`openstack  floating ip create public | awk '/ floating_ip_address / {print $4}'`
echo got ${floating_ip} sleeping for sync
sleep 15

# Associate floating IP with server
openstack  server add floating ip obs ${floating_ip}

echo "A Xenial instance should be available on ${floating_ip}"
echo "try accessing via ssh from controller: ubuntu@${floating_ip}"


