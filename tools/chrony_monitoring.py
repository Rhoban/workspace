#! /usr/bin/env python
import sys
import os
from time import sleep
import datetime

if len(sys.argv) < 2:
    print('Usage: time_client.pt [host1] [host2]')
    exit()

hosts = []
for host in sys.argv[1:]:
    hosts.append(host)

initial_local_time = float(datetime.datetime.now().timestamp())
while True:
    sleep(0.5)
    local_time = float(datetime.datetime.now().timestamp()) - initial_local_time
    msg = ""
    msg += str(local_time)
    msg += " "
    for host in hosts:
        offset = float(os.popen("ssh rhoban@%s chronyc -n -c sources" %host).readline().split(",")[-3])
        msg += str(offset * 1000)
        msg += " "
    print(msg[:-1])
    sys.stdout.flush()
