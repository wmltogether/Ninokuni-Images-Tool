# -*- coding: utf-8 -*-
import os
import struct
from binaryIO import BinaryReader
from GIDecode import getPaletteData , paint8BPP,setAlphaPalette256
from PIL import Image

def gen_p3img(filename):
    if not os.path.exists("table"):
        os.makedirs("table")
    if not os.path.exists("unpacked"):
        os.makedirs("unpacked")
    if not os.path.exists("png"):
        os.makedirs("png")
    table_file = open("table\\%s.csv"%(filename.replace("\\" , "@@")), 'wb')
    fp = open(filename , 'rb')
    fStream = BinaryReader(fp)

    name = filename[:-3]
    name_igg = name + 'igg'
    name_img = name + 'img'
    sig = "\x69\x6d\x67\x00" # img\x00
    fStream.seek(0x10)
    BASEOFF = fStream.ReadBEInt32()
    fStream.seek(0x28)
    FILES = fStream.ReadBEInt32()
    fStream.seek(0x30)
    SKIPOFF = fStream.ReadBEInt32()
    STARTOFF = BASEOFF
    STARTOFF += SKIPOFF
    img_dict = {}
    plt_dict = {}
    for i in xrange(FILES):
        fStream.seek(STARTOFF)
        NAMEOFF = fStream.ReadBEInt32()
        NAMEOFF += BASEOFF
        # 0X1C
        OFFSET = fStream.ReadBEInt32()
        SIZE = fStream.ReadBEInt32()
        DUMMY = fStream.ReadBEInt32()
        TYPE = fStream.ReadBEInt32()
        FILENUM = fStream.ReadBEInt32()
        WIDTH = fStream.ReadBEInt16()
        HEIGHT = fStream.ReadBEInt16()
        USLS = fStream.ReadBytes(0x14)
        STARTOFF = fStream.tell()
        Pixel_data = ""
        Palette_data = ""
        image_name = ""
        if TYPE == -1593769472:
            # is Pixel table
            TWIDTH = WIDTH
            THEIGHT = HEIGHT

            TSIZE = SIZE
            if "t02.p3img" in filename.lower():
                TWIDTH = TWIDTH / 2
                THEIGHT = THEIGHT /2
                SIZE = SIZE /4
            TYPE_NAME = 'PIXEL'
            Pixel_data = logPixel(name_igg ,OFFSET , SIZE)
            fStream.seek(NAMEOFF)
            DATA_NAME = fStream.GetcString()
            image_name = DATA_NAME
            destimg_name = 'unpacked\\%s[%s]'%(name_igg.replace("\\" , "__") , image_name)
            img_dict[image_name] = (Pixel_data , TWIDTH , THEIGHT, OFFSET , SIZE , destimg_name)
            dest = open(destimg_name , 'wb')
            dest.write(Pixel_data)
            dest.close()
            
        if TYPE == -1526660608:
            # is Palette table
            TYPE_NAME = 'PALATTE_256'
            Palette_data = logPalette(name_igg , OFFSET ,SIZE)
            fStream.seek(NAMEOFF)
            DATA_NAME = fStream.GetcString()
            destplt_name = 'unpacked\\%s[%s]'%(name_igg.replace("\\" , "__") , DATA_NAME)
            plt_dict[DATA_NAME] = (Palette_data , OFFSET , SIZE , destplt_name)
            dest = open(destplt_name, 'wb')
            dest.write(Palette_data)
            dest.close()
            
    for key in img_dict:
        image_name = key
        palette_name = key+"_plt"
        if palette_name in plt_dict:
            # match Palette
            (Pixel_data , TWIDTH , THEIGHT, I_OFFSET , I_SIZE , destimg_name) = img_dict[image_name]
            (Palette_data , P_OFFSET , P_SIZE , destplt_name) = plt_dict[palette_name]
            palette_list = getPaletteData(Palette_data,0xff,4,False,0)
            if "t02.p3img" in filename.lower():
                palette_list = setAlphaPalette256()
            pixel_list = paint8BPP(TWIDTH , THEIGHT,TWIDTH , THEIGHT,Pixel_data,palette_list,"linear",256 , 1,"PS3")
            im = Image.new('RGBA', (TWIDTH , THEIGHT))
            im.putdata(tuple(pixel_list))
            PNG_NAME = "png\\%s[%s].png"%(name_igg.replace("\\" , "__") , image_name)
            im.save(PNG_NAME)
            table_file.write("%s\t%s\t%08x\t%08x\t%08x\t%08x\t%s\t%s\r\n"%(PNG_NAME ,
                                       name_igg ,
                                       I_OFFSET ,
                                       I_SIZE ,
                                       P_OFFSET ,
                                       P_SIZE,
                                       destimg_name,
                                       destplt_name))

    table_file.close()
    fp.close()


def logPixel(name_igg ,OFFSET , SIZE):
    fp = open(name_igg , 'rb')
    fp.seek(OFFSET)
    Pixel_data = fp.read(SIZE)
    fp.close()
    return Pixel_data

def logPalette(name_igg ,OFFSET , SIZE):
    fp = open(name_igg , 'rb')
    fp.seek(OFFSET)
    Palette_data = ""
    for i in xrange(0x100):
        a = fp.read(1)
        b = fp.read(1)
        c = fp.read(1)
        d = fp.read(1)
        Palette_data += (b + c + d + a)
    fp.close()
    return Palette_data

def logSpecialPalette():
    Palette_data = ""
    for i in xrange(0x100):
        a = chr(0)
        b = chr(0)
        c = chr(0)
        d = chr(i)
        Palette_data += (b + c + d + a)
    return Palette_data


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




