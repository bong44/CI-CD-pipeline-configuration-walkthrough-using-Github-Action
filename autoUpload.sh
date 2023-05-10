#!/bin/bash

if [ $# -eq 1 ]; then
  cntxt=$1
  echo "#!/bin/bash" > tuneindex.sh;echo "cat /usr/share/nginx/html/${cntxt} > /usr/share/nginx/html/index.html" >> tuneindex.sh
fi

msg=$(date +"%Y-%m-%d %T")" content edit"

git add . && git commit -m " $msg " && git push origin master