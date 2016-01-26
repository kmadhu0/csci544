from pprint import pprint
from sys import argv
op_file=argv[2]
file1 = open(op_file, 'wb')
scale = 16 ## equals to hexadecimal
num_of_bits = 16

#reading the input file
file=argv[1]
with open(file, "rb") as f:
    #reading two bytes at once as in UTF-16, 2 bytes correspond to one character
    byte = f.read(2)
    while byte != "":
        #obtain the code point
        a=hex(ord(byte[0]))
        b=hex(ord(byte[1]))
        if len(a)==4:
            a=a[2:]
        else:
            a=a[2:]
            a="0"+a
        if len(b)==4:
            b=b[2:]
        else:
            b=b[2:]
            b="0"+b
        c="0x"+a+b
        #check is the integer value of the code point
        check=int(c,0)

        #code point in binary
        d=bin(int(c, scale))[2:].zfill(num_of_bits)

        #find the range of the code point
        if check>=0 and check<=127:
            #U+0000 to U+007F
            a1="0" #higher order bit
            d=d[1:]
            temp1=a1+d
            temp1_hex=chr(int(temp1,2)) #converting from hex integer to hex string
            final=temp1_hex
            file1.write(final)
        elif check>=128 and check<=2047:
            #U+0080 to U+07FF
            b1="110" #b1 and b2 are the higher order bits
            b2="10"
            d=d[5:]
            temp1=b1+d[0:5]
            temp2=b2+d[5:]
            temp1_hex=chr(int(temp1,2)) #converting from hex integer to hex string
            temp2_hex=chr(int(temp2,2))
            final=temp1_hex+temp2_hex
            file1.write(final)
        elif check>=2048 and check<=65535:
            #U+0800 to U+FFFF
            c1="1110" #c1, c2 and c3 are the higher order bits
            c2="10"
            c3="10"
            temp1=c1+d[0:4]
            temp2=c2+d[4:10]
            temp3=c3+d[10:]
            temp1_hex=chr(int(temp1,2)) #converting from hex integer to hex string
            temp2_hex=chr(int(temp2,2))
            temp3_hex=chr(int(temp3,2))
            final=temp1_hex+temp2_hex+temp3_hex
            file1.write(final)
        byte = f.read(2)
