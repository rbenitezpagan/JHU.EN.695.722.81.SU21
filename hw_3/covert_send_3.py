######################################################################
# Course..: Covert Channels                                          #
# ID......: #######                                                  #
# Student.: Ramon Benitez-Pagan                                      #
#                                                                    #
# <covert_send_3.py>                                                 #
# Implements a custom covert channel by sending data using TFTP      #
######################################################################

import os, sys, subprocess, socket, random, string, uuid

######################################################################
# get_ip() snippet retrieved from:                                   #
# URL: stackoverflow.com/questions/166506/finding-local-ip-addresses #
# -using-pythons-stdlib                                              #
######################################################################

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


######################################################################
# CUSTOM CODE DEVELOPMENT                                            #
######################################################################

def sendMyFile(dst,myFileLoc):
    subprocess.call([
        'curl',
        '-T',
        myFileLoc,
        'tftp://'+str(dst)+'/'
    ])

# myMsg = "HolaHOLAHOlahoLAHh"
DST = str(sys.argv[1])
myMsg = str(sys.argv[2])
myChunks = int(len(myMsg)/4) if (int(len(myMsg)%4) == 0) else (int(len(myMsg)/4)+1)

myFinalData = []

for x in range(0, myChunks):
    myChunkData = myMsg[x*4:(x*4)+4]
    while len(myChunkData) < 4:
        myChunkData = myChunkData + "_"
    
    myFinalData.append(myChunkData)

myMsgHex = myMsg.encode("utf-8").hex()
myIP = myIP2 = get_ip()
print(myIP)
myIP = myIP.split(".")
# print("010.000.002.005")
print("_X_._X_.__X.__X")
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
myXORDataDec = []
for chunk in myFinalData:
    myChunkHex = chunk.encode("utf-8").hex()
    myChunkBin = "{:0>32}".format(bin(int(myChunkHex, 16))[2:])
    exclu = "{:0>32}".format(bin(int(myChunkBin,2) ^ int(myKeyBin,2))[2:])
    myXORData.append(exclu)
    
    print(chunk)
    print("Key bin: ",myKeyBin)
    print("chk bin: ",myChunkBin)
    print("XOR bin: ",exclu)

myFileId = uuid.uuid4()

f = open("/tmp/"+str(myFileId)+".txt", "w")

f.write(str(myIP2)+':'+"0000000000"+"\n")

# send(myIP2,DST,)

for x in range(0, len(myXORData)):
    myXORDataDec.append(int(myXORData[x],2))
    f.write(str(myIP2)+':'+str(myXORDataDec[x])+"\n")


f.write(str(myIP2)+':'+"4294967295"+"\n")
f.close()

sendMyFile(DST, "/tmp/"+str(myFileId)+".txt")

print("Data:", myXORDataDec)
print()
print("Finished.")

######################################################################
# References:                                                        #
# [0] gist.github.com/NickKaramoff/b06520e3cb458ac7264cab1c51fa33d6  #
# [1] stackoverflow.com/questions/166506/finding-local-ip-addresses  #
# -using-pythons-stdlib                                              #
# [2] binarytides.com/raw-socket-programming-in-python-linux/        #
#                                                                    #
######################################################################