import os
import sys

def decode(isn):
    # print(isn)
    myISNBin = "{:0>32}".format(bin(isn)[2:])
    # print(myISNBin)
    # print(myKeyBin)
    myLeakedBin = "{:0>32}".format(bin(int(myISNBin,2) ^ int(myKeyBin,2))[2:])
    # print(myLeakedBin)
    myLeakedHex = hex(int(myLeakedBin,2))[2:]
    # print(myLeakedHex)
    myLeakedBytes = bytes.fromhex(myLeakedHex)
    # print(myLeakedBytes)
    myLeakedMsg.append(myLeakedBytes.decode('ASCII'))
    # print(myLeakedBytes.decode('ASCII'))

myLeakedMsg = []

myIP = str(sys.argv[1]).split('_')[-1]
myIP = myIP.split(".")
myIP[0] = '{:0>3}'.format(myIP[0])[1]
myIP[1] = '{:0>3}'.format(myIP[1])[1]
myIP[2] = '{:0>3}'.format(myIP[2])[2]
myIP[3] = '{:0>3}'.format(myIP[3])[2]

myKey = "".join(myIP)
myKeyHex = myKey.encode("utf-8").hex()
myKeyBin = "{:0>32}".format(bin(int(myKeyHex, 16))[2:])
myKeyDec = int(myKeyBin,2)

f = open(str(sys.argv[1]), "r")
myXORData =  f.readlines()
# print(len(myXORData))

for line in myXORData:
    if int(line.strip('\n')) == 0 or int(line.strip('\n')) == 4294967295:
        continue
    else:
        decode(int(line.strip('\n')))


myLeakedMsgStr = "".join(myLeakedMsg)
print(myLeakedMsgStr)

exit()

myFinalData = []

for x in range(0, myChunks):
    myChunkData = myMsg[x*4:(x*4)+4]
    while len(myChunkData) < 4:
        myChunkData = myChunkData + "_"
    
    myFinalData.append(myChunkData)
    # print(myFinalData)

myMsgHex = myMsg.encode("utf-8").hex()
# print(myMsgHex)
# chunks = [str[i:i+n] for i in range(0, len(str), n)]

DST = '10.0.2.4'

myIP = get_ip()
print(myIP)
myIP = myIP.split(".")
myIP[0] = '{:0>3}'.format(myIP[0])[1]
myIP[1] = '{:0>3}'.format(myIP[1])[1]
myIP[2] = '{:0>3}'.format(myIP[2])[2]
myIP[3] = '{:0>3}'.format(myIP[3])[2]

myKey = "".join(myIP)
myKeyHex = myKey.encode("utf-8").hex()
myKeyBin = "{:0>32}".format(bin(int(myKeyHex, 16))[2:])
myKeyDec = int(myKeyBin,2)

print("My IP:",myIP)
print("My key:",myKey)
print("My key hex:",myKeyHex)
print("My key bin:",myKeyBin)
print("My key dec:",myKeyDec)

myXORData = []

for chunk in myFinalData:
    myChunkHex = chunk.encode("utf-8").hex()
    myChunkBin = "{:0>32}".format(bin(int(myChunkHex, 16))[2:])
    exclu = "{:0>32}".format(bin(int(myChunkBin,2) ^ int(myKeyBin,2))[2:])
    myXORData.append(exclu)
    
    print(chunk)
    print("Key bin: ",myKeyBin)
    print("chk bin: ",myChunkBin)
    print("XOR bin: ",exclu)