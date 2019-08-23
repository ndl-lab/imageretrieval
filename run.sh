#!/bin/bash
#service supervisor start
nohup /root/go/bin/ngtd  http -i /root/ngt/imgindex -d 1280 -t bolt -p /root/ngt/kvs.bdb -P 10000 > /dev/null 2>&1
