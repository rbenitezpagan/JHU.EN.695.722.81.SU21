######################################################################
# Course..: Covert Channels                                          #
# ID......: #######                                                  #
# Student.: Ramon Benitez-Pagan                                      #
#                                                                    #
# <covert_send.py>                                                   #
# Implements a custom covert channel by sending data in the TCP      #
# header field: Initial Sequence Number (ISN)                        #
######################################################################

import os
import sys

######################################################################
# tcp.py retrieved from:                                             #
# URL: gist.github.com/NickKaramoff/b06520e3cb458ac7264cab1c51fa33d6 #
######################################################################

# tcp.py -- example of building and sending a raw TCP packet
# Copyright (C) 2020  Nikita Karamov  <nick@karamoff.dev>
#
# With code from Scapy (changes documented below) 
# Copyright (C) 2019  Philippe Biondi <phil@secdev.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import array
import socket
import struct

# This part of code was adapted from the Scapy project:
# https://github.com/secdev/scapy/blob/467431faf8389f745d2c16370baf6dafc5751731/scapy/utils.py#L368-L381
#
# Changes made:
# - removed use of checksum_endian_transform function
# - restructured code without modifying it
# - renamed variables
# - added type hints
def chksum(packet: bytes) -> int:
    if len(packet) % 2 != 0:
        packet += b'\0'

    res = sum(array.array("H", packet))
    res = (res >> 16) + (res & 0xffff)
    res += res >> 16

    return (~res) & 0xffff


class TCPPacket:
    def __init__(self,
                src_host:  str,
                src_port:  int,
                dst_host:  str,
                dst_port:  int,
                ######################################################
                # Modified to include the arbitrary ISN.
                myISN:     int,
                ######################################################
                flags:     int = 0):
        self.src_host = src_host
        self.src_port = src_port
        self.dst_host = dst_host
        self.dst_port = dst_port
        self.myISN = myISN
        self.flags = flags

    def build(self) -> bytes:
        packet = struct.pack(
            '!HHIIBBHHH',
            self.src_port,  # Source Port
            self.dst_port,  # Destination Port
            # 0,              # Sequence Number
            ##########################################################
            # Modified to include the arbitrary ISN.
            self.myISN,     # My Sequence Number
            ##########################################################
            0,              # Acknoledgement Number
            5 << 4,         # Data Offset
            self.flags,     # Flags
            8192,           # Window
            0,              # Checksum (initial value)
            0               # Urgent pointer
        )

        pseudo_hdr = struct.pack(
            '!4s4sHH',
            socket.inet_aton(self.src_host),    # Source Address
            socket.inet_aton(self.dst_host),    # Destination Address
            socket.IPPROTO_TCP,                 # PTCL
            len(packet)                         # TCP Length
        )

        checksum = chksum(pseudo_hdr + packet)

        packet = packet[:16] + struct.pack('H', checksum) + packet[18:]

        return packet


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

def send(ip,isn):
    pak = TCPPacket(
        ''.join(ip),
        20,
        DST,
        666,
        ##############################################################
        # Modified the code to send the arbitrary ISN in constructor.
        isn,
        ##############################################################
        0b000101001  # Merry Christmas!
    )
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    s.sendto(pak.build(), (DST, 0))

# myMsg = "HolaHOLAHOlahoLAHh"
myMsg = str(sys.argv[1])
myChunks = int(len(myMsg)/4) if (int(len(myMsg)%4) == 0) else (int(len(myMsg)/4)+1)

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

send(myIP,0000000000)

for x in range(0, len(myXORData)):
    myXORDataDec.append(int(myXORData[x],2))
    send(myIP,myXORDataDec[x])

send(myIP,4294967295)

print("ISNs to send are:", myXORDataDec)
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