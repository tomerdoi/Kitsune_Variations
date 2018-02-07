import numpy as np
import os

dpath='C:/Users/tomerdoi/Desktop/MT_Video'
files=os.listdir(dpath)

for f in files:
    parts=f.split('.')
    num=int(parts[0])
    num=int(num/100)
    os.rename(str(dpath)+'/'+str(f),str(dpath)+'/'+str(num)+'.png')