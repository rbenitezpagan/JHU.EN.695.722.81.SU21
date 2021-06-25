#!/bin/bash

# Data collected by using 'sudo tcpdump -S src 10.0.2.5 > 10.0.2.5.txt'

ip=$(echo $1 | grep -oP '([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})')

cat $1 | cut -d' ' -f 3,9 > ext_data_1_$ip

cat ext_data_1_$ip | grep -oP '(([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})|([0-9]{1,10}))' > ext_data_2_$ip

cat ext_data_2_$ip | grep -oP '(\A[0]\Z|\A[0-9]{10}\Z)' > ext_data_$ip

rm ext_data_1_$ip
rm ext_data_2_$ip
