import numpy as np
import cv2
import sys
import time
import glob
import os


if(len(sys.argv) ==  3):
    export_path = sys.argv[2]
    if(not(export_path[len(export_path)-1] == '/')):
        export_path = export_path+'/'
else:
    print("USAGE : python yuv2rgb.py <path_to_yuv_images> <export_path>")
    sys.exit()

path_folder = sys.argv[1]
if(not(path_folder[len(path_folder)-1] == '/')):
    path_folder = path_folder+'/'
i=0
    
for _, f in enumerate(sorted(os.listdir(path_folder))):
    if f.endswith(".png"):
        f = path_folder+f
        print(f)
        img = cv2.imread(f,1)
        img = cv2.cvtColor(img, cv2.COLOR_YUV2RGB)
        cv2.imwrite(export_path+str(i)+".png", img)
        i+=1

    
print("DONE : Files written to "+export_path)
