from PIL import Image
import os, sys

path = "images/"
op = "resized/"
dirs = os.listdir( path )

def resize():
    for item in dirs:
        if os.path.isfile(path+item):
            im = Image.open(path+item)
            im = im.convert('RGB')
            f, e = os.path.splitext(path+item)
            save = 'resized'+str(f[6:])
            imResize = im.resize((400,400), Image.ANTIALIAS)
            if save+'.jpg' not in os.listdir(op):
                imResize.save(save+'.jpg', 'jpeg', quality=80)