# -*- coding: utf-8 -*-
from PIL import Image
from GIDecode import create8BPP , getPaletteData , setAlphaPalette256
import os
import csv
import shutil
from p3igg import logPalette

def getCSVinfo(pngname):
    iggname = pngname.split("[")[0]
    imgname = iggname[:-3] + 'img'
    table_name = "table\\%s.csv"%(imgname.replace("__" , "@@"))
    with open(table_name, 'rb') as csvfile:
        csvReader = csv.reader(csvfile)
        for row in csvReader:
            while "%s"%pngname in row[0]:
                row = row[0].replace("\r\n" , "")
                (o_pngname,\
                    o_iggname,\
                    I_OFFSET,\
                    I_SIZE,\
                    P_OFFSET,\
                    P_SIZE,\
                    o_piexl_name,\
                    plt_name)= tuple(row.split("\t")[:8])
                I_OFFSET = int(I_OFFSET , 16)
                P_OFFSET = int(P_OFFSET , 16)
                I_SIZE = int(I_SIZE , 16)
                P_SIZE = int(P_SIZE , 16)
                return (I_OFFSET , I_SIZE , P_OFFSET , P_SIZE , o_iggname)
                break


def png2igg(pngname):
    iggname = pngname.split("[")[0]
    imgname = iggname[:-3] + 'img'

    im = Image.open("CNPNG\\%s"%pngname).convert("RGBA")
    TWIDTH , THEIGHT = (im.size[0] , im.size[1])
    src = iggname.replace("__" , "\\")
    dst = "import\\%s"%src
    if not os.path.exists(dst):
        os.makedirs(("\\".join(dst.split("\\")[:-1])))
        shutil.copy(src , dst)
    getCSVinfo(pngname)
    (I_OFFSET , I_SIZE ,P_OFFSET, P_SIZE, o_iggname) = getCSVinfo(pngname)
    paletteData = logPalette(o_iggname ,P_OFFSET, P_SIZE)
    if "t02.p3img" in imgname.lower():
        paletteList = setAlphaPalette256()
    else:
        paletteList = getPaletteData(paletteData,0xff,4,False,0)
    imdata = create8BPP(TWIDTH , THEIGHT,TWIDTH , THEIGHT,im,paletteList,"RGBA",16,16)
    if len(imdata) <= I_SIZE:
        print("write:%s >> %s"%(pngname , dst))
        dest = open(dst , "rb+")
        dest.seek(I_OFFSET)
        dest.write(imdata)
        dest.close()
    else:
        print("error:image length error %s"%(pngname))

def dir_fn(adr ,ext_name):
    dirlst=[]
    for root,dirs,files in os.walk(adr):
        for name in files:
            ext = name.split('.')[-1]
            adrlist=os.path.join(root, name)
            if ext.lower() in ext_name:
                dirlst.append(adrlist)
    return dirlst

def main():
    if not os.path.exists("cnpng"):
        os.makedirs("cnpng")
    if not os.path.exists("import"):
        os.makedirs("import")
    fl = dir_fn("cnpng" , "png")
    for fn in fl:
        print(fn[6:])
        png2igg(fn[6:])

if __name__ == "__main__":
    main()





