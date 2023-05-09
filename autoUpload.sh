#!/bin/bash

read -p "콘솔 입력 _ 커밋 메세지를 입력해주세요: " msg
git add . && git commit -m " $msg " && git push origin master