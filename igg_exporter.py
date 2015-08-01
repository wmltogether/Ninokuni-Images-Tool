import os
from p3igg import gen_p3img

def dir_fn(adr ,ext_name):
    dirlst=[]
    for root,dirs,files in os.walk(adr):
        for name in files:
            ext = name.split('.')[-1]
            adrlist=os.path.join(root, name)
            if ext.lower() in ext_name:
                dirlst.append(adrlist)
    return dirlst

if not os.path.exists("data"):
    os.makedirs("data")
fl = dir_fn("data" , "p3img")
for fn in fl:
    gen_p3img(fn)

