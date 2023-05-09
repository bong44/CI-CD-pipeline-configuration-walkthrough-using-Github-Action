#!/bin/bash

if [ $# -eq 1 ]; then
  msg=$1
else
  msg=$(date +"%Y-%m-%d %T")" content edit"
fi

echo $msg

git add . && git commit -m " $msg " && git push origin master