#!/bin/bash

echo 'starting 1'
nohup python crawler.py &

echo 'starting 2'
nohup python poster.py &
