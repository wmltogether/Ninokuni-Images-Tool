# -*- coding: utf-8 -*-
import struct
import cStringIO
class BinaryReader:
    def __init__(self , base_stream):
        self.base_stream = base_stream

    def seek(self,count):
        return self.base_stream.seek(count)

    def tell(self,):
        return self.base_stream.tell()

    def ReadByte(self):
        return self.base_stream.read(1)
    
    def ReadBytes(self , count):
        return self.base_stream.read(count)    
    
    def ReadChar(self):
        return ord(self.base_stream.read(1))
    
    def ReadChars(self , count):
        return struct.unpack('%dB' , self.base_steam.read(count))
    
    def ReadInt16(self):
        return struct.unpack('h' , self.base_stream.read(2))[0]
    
    def ReadInt32(self):
        return struct.unpack('i' , self.base_stream.read(4))[0]
    
    def ReadInt64(self):
        return struct.unpack('q' , self.base_stream.read(8))[0]

    def ReadUInt16(self):
        return struct.unpack('H' , self.base_stream.read(2))[0]
    
    def ReadUInt32(self):
        return struct.unpack('I' , self.base_stream.read(4))[0]
    
    def ReadUInt64(self):
        return struct.unpack('Q' , self.base_stream.read(8))[0]
    
    def ReadFloat(self):
        return struct.unpack('f' , self.base_stream.read(4))[0]
    
    def ReadBEInt16(self):
        return struct.unpack('>h' , self.base_stream.read(2))[0]
    
    def ReadBEInt32(self):
        return struct.unpack('>i' , self.base_stream.read(4))[0]
    
    def ReadBEInt64(self):
        return struct.unpack('>q' , self.base_stream.read(8))[0]

    def ReadBEUInt16(self):
        return struct.unpack('>H' , self.base_stream.read(2))[0]
    
    def ReadBEUInt32(self):
        return struct.unpack('>I' , self.base_stream.read(4))[0]
    
    def ReadBEUInt64(self):
        return struct.unpack('>Q' , self.base_stream.read(8))[0]

    def GetcString(self):
        cString = ""
        while True:
            char = self.base_stream.read(1)
            if char == '\x00':
                break
            else:
                cString += char
        return cString

    def Read7BitEncodedInt(self):
        a , b, c = 0 , 0 ,0
        mask = 0x7f
        shift = 7
        while c < 5:
            d = ord(self.ReadByte())
            a |= (d & mask) << b
            b += shift
            if ((d & (mask + 1 )) == 0):
                break
            c += 1
            
        if c >= 5:
            raise NameError, ("Too many bytes in what should have been a 7 bit encoded Int32")
        return a
    
    def ReadString(self):
        capacity = self.Read7BitEncodedInt()
        if capacity < 0:
            raise IOError,("Invalid binary file (string len < 0)")
        if capacity == 0 :
            return ""
        string_buffer = self.ReadBytes(capacity)
        return string_buffer
    
class BinaryWriter:
    def __init__(self , base_stream):
        self.base_stream = base_stream

    def WriteByte(self , value):
        self.base_stream.write(value[0])
    
    def WriteBytes(self , value , count):
        if count <= 0:
            count = 0
        if len(value) <= count:
            value += '\x00' * (count - len(value))   
        self.base_stream.write(value[:count])
        
    def Write7BitEncodedInt(self , value):
        if value == 0:
            self.WriteByte(chr(value))
        while value != 0:
            num =  (value >> 7) & 0x1ffffff;
            num2 = value & 0x7f
            if num != 0:
                num2 = num2 | 0x80
            self.WriteByte(chr(num2))
            value = num
            
    def WriteString(self , value):
        byteCount = len(value)
        self.Write7BitEncodedInt(byteCount)
        self.WriteBytes(value , len(value))

