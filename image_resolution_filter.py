import imagesize
import shutil
import os
from os import listdir, mkdir
from os.path import isfile, join


imagefiles = [f for f in listdir("./") if isfile(join("./", f)) and f.endswith((".jpg",".png", ".jpeg", ".webp"))]

if not os.path.exists("./_lowres"):
    mkdir("./_lowres")

for f in imagefiles:
    width, height = imagesize.get(f)
    if width < 1000 or height < 1800:
        print("Move: " + f + " " + str(width) + " " + str(height))
        shutil.move("./"+f, "./_lowres/"+f)
               