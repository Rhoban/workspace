#!/usr/bin/env python3
import sys
import os
import re
from utils import *


print("retrieving robot's name throught rhio...")

ip: str = "10.0.0.1" if len(sys.argv) == 1 else sys.argv[1]
hostname: str = rhio_get_value(ip, "/server/hostname")

print(ip,hostname)

motors=["hip_pitch","hip_yaw","hip_roll","knee","ankle_pitch","ankle_roll"]

def print_zero(sides):
    for side in sides:
        for m in motors:
            print(rhio(ip, f"/lowlevel/{side}_{m}/position"))

        
# setting parameters to zero
def update_zero(sides):
    for side in sides:
        for m in motors:
            rhio(ip, f"/lowlevel/{side}_{m}/parameters/zero=0")
        
    for side in sides:
        for m in motors:
            p=rhio(ip, f"/lowlevel/{side}_{m}/position").split('=')[1]
            rhio(ip, f"/lowlevel/{side}_{m}/parameters/zero={p}")

def save_zero():
    rhio(ip,"rhalSaveConf rhal.json")

sides=["left","right"]
    
while True:
    a=input("(p)rint/(u)pdate/(s)ave/(q)uit?")
    a=a.strip()
    if a=="p":
        print_zero(sides)
    elif a=="u":
        update_zero(sides)
    elif a=="s":
        save_zero()
    elif a=="q":
        sys.exit(1)
