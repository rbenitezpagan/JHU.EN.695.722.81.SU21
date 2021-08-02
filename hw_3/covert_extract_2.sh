#!/bin/bash

cat $2 | cut -d':' -f 2 > ext_data_1_$1
cat ext_data_1_$1 | grep -oP '(\A[0]\Z|\A[0-9]{10}\Z)' > ext_data_$1
rm ext_data_1_$1
