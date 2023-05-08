#!/bin/bash

# 변수 정의
CONTAINER_NAME="test"
IMAGE_NAME="bongzzang/bong:test"
PORT_MAPPING="38080:80"

# 허브에 빌드 후 푸시
sudo docker build -t $IMAGE_NAME .
sudo docker push $IMAGE_NAME

# Docker 이미지 가져오기
docker pull $IMAGE_NAME

# 컨테이너가 존재하는지 확인
if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
    # 컨테이너가 실행 중이면 업데이트
    sudo docker container stop $CONTAINER_NAME
    sudo docker container rm $CONTAINER_NAME
fi

# 컨테이너 실행
sudo docker container run -d --restart always --name $CONTAINER_NAME -p $PORT_MAPPING $IMAGE_NAME
