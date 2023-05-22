# Web Programming Practice & CI/CD auto pipeline build useing Git and Jenkins

**This repo aims to practice to build a pipeline that useing git, jenkins, docker, linux shell and network programming skill.
On this README file, explained how to set pipeline:**

  - Network setting
  - Local repository setting
  - Git Hub setting
  - Jenkins setting<br><br>
  
  <img src="https://img.shields.io/badge/docker-3776AB?style=for-the-badge&logo=docker&logoColor=white"><img src="https://img.shields.io/badge/jenkins-F2CB61?style=for-the-badge&logo=jenkins&logoColor=white"><img src="https://img.shields.io/badge/git-76B900?style=for-the-badge&logo=git&logoColor=white"><img src="https://img.shields.io/badge/centos-262577?style=for-the-badge&logo=centos&logoColor=white"><img src="https://img.shields.io/badge/shell-FFD500?style=for-the-badge&logo=shell&logoColor=white"><img src="https://img.shields.io/badge/slack-4A154B?style=for-the-badge&logo=slack&logoColor=white">
 
# requirement
  - CentOS(also Virtual CentOS) 
    - Jenkins Server installed
    - Docker installed
  - GitHub repository
  - DockerHub repository

# Outcome

  - **http://[CentOS IP:포워딩된 포트]/[html파일의 경로] 와 같은 방식으로 웹에서 접근할 수 있도록 구성**

# Getting start

- Describes various settings for configuring the pipeline and how to execute it

## Network setting

  0. 가상머신일 경우 network setting을 bridged가 아닌 NAT로 설정

  1. CentOS의 8080(젠킨스 포트)와 앞으로 만들어질 임의의 컨테이너 포트포워딩 설정 (본인은 가상머신을 사용하여 호스트 OS의 내부포트와 연결시키줌)
  
![image](https://user-images.githubusercontent.com/65393001/236975695-4cd22293-95ed-4ad9-8d05-05c5ccb2f8ef.png)

  1-2. [가상머신 사용시] 호스트 OS의 내부포트와 외부포트를 포트포워딩 ⚠️ * 꼭 자신의 아이피로 설정 *

![image](https://user-images.githubusercontent.com/65393001/236980568-2486718d-0b75-46df-ba7c-07292823436a.png)

    - 편의를 위해 DDNS 설정 (안 하면 외부 아이피를 사용해야 함)
      ex) http://test.iptime.org:38080/test.html 와 같이 접근 가능
    
   ![image](https://user-images.githubusercontent.com/65393001/236981165-4b7e0ac9-55e2-4904-8f2d-b266686b8531.png)

  2. CentOS와 호스트OS의 인바운드 규칙에 포트번호 추가 (방화벽 off 해도 가능하지만 비권장) ⚠️ * 보안프로그램 방화벽 또한 off *

## Local repository setting

  0. 깃허브에 올라갈 Dockerfile 등 파이프라인 구성에 필요한 파일 작성 (Dockerfile)
      ```Dockerfile
      FROM nginx
      ADD ./ /usr/share/nginx/html
      EXPOSE 80
      ```
      0-1. Jenkins 의 exec shell에서 실행될 파일 작성 (dockergenerater.sh)
  
     ```sh
      #!/bin/bash

      # 변수 정의
      CONTAINER_NAME="[컨테이너명]"
      IMAGE_NAME="[도커허브ID]/[repo이름]:[태그명]"
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

      ```
      
      0-2. 깃 push 자동화 실행파일 코드 (auroUpload.sh)
      
      ```sh
        #!/bin/bash

        if [ $# -eq 1 ]; then
        msg=$1
        else
        msg=$(date +"%Y-%m-%d %T")" content edit"
        fi

        echo $msg

        git add . && git commit -m " $msg " && git push origin master
      ```
  1. 깃 repository와 연결 (윈도우는 git bash를 사용)
    
    ```sh
      $ git init
      $ git remote add origin https://github.com/[GIT프로필]/[repo이름].git
      ```

## Git Hub setting

  0. 깃허브에 생성한 repo의 setting -> webhook 아래와 같이 설정 (후에 Jenkins 서버의 build Trigger에 필요) 
  
  ![image](https://user-images.githubusercontent.com/65393001/236983194-859396a0-07b4-41eb-835d-45846318e76a.png)
  
  1. Jenkins server와 연결의 위한 Token 아래와 같이 생성. 우측상단 프로필 -> settings -> Developer setting -> (classic) Token
  
  ![image](https://user-images.githubusercontent.com/65393001/236984441-8c5bdbe0-0b3d-4ba9-9fec-2522f045464a.png)
  
  ⚠️ * 생성시 토큰 보여주고 다음번엔 알 수 없기에 잘 보관 *
  
## Jenkins setting

  0. Jenkins 관리 -> 플러그인 관리 -> 'github integration' 플러그인 설치
  
  ![image](https://user-images.githubusercontent.com/65393001/236992979-88b9a1c6-2f53-4a22-a872-ec36a46bbed9.png)

  2. Jenkins 관리 -> 시스템 설정 -> Git server에서 add server 
  
  ![image](https://user-images.githubusercontent.com/65393001/236993753-cfbc7e10-0876-42a6-a5cd-8237ec6c5453.png)
  
  kind는 secret text, git Token 입력
  
  ![image](https://user-images.githubusercontent.com/65393001/236993981-c026bcca-ad7a-4e42-b99a-573a4662ff97.png)
  
  3. 만들어놓은 Jenkins Project -> 구성 -> 소스코드 관리 -> git으로 설정 후 Credentials탭에 Add -> kind 'Username with password'로 토큰 생성
  
  ![image](https://user-images.githubusercontent.com/65393001/236995500-da13c06f-4ed5-4c89-becf-fca723869a8f.png)
  
  4. 구성 -> 빌드유발 'GitHub hook trigger for GITScm polling' 체크
  
  5. 구성 -> Build step 에서 Add build step - Execute shell 추가 후 아래와 같이 구성

  ![image](https://user-images.githubusercontent.com/65393001/236995941-541ef52d-bd3e-4fbe-b0a9-6237fef4f4a1.png)
  
## How to use

  - C:\User\Kosta\[파일경로]> .\auroUpload.sh [커밋메세지 (선택사항)]  <-- 인수로 커밋 메세지 넣어서 실행 가능

### Tips
  
  - 아래와 같은 방법으로 Slack을 통해 build process Notification 구성 가능.

    https://dnight.tistory.com/entry/Jenkins-Slack-%EC%95%8C%EB%A6%BC-%EC%97%B0%EB%8F%99

  - CentOS의 Docker 컨테이너안에 깃에서 받아온 정보가 잘 들어갔는지 아래와 같이 확인할 수 있다.
    
    ```sh
      $ docker exec -it [컨테이너 ID] /bin/bash
      # 컨테이너 bin/bash 에 진입
      root@[컨테이너 ID]:# ls -al /usr/share/nginx/html
      ```
  - CentOS 로컬환경에서 아래와 같은 방법으로 스크립트를 사용하여 빌드를 유발시킬 수 있다.

    ```sh
      $ java -jar jenkins-cli.jar -s http://[Jenkins가 설치된 컴퓨터의 IP]:[Jenkins포트]/ build WebStudyAtMetanet -s -v
      ```
      
      ⚠️ * 앞서, 위 명령어를 사용하기 위해선 Jenkins Cli 플러그인이 필요하다. (따로 설치 필요) *
      
      https://qaautomation.expert/2022/12/21/how-to-install-plugins-from-jenkins-cli/
      
   - 위 환경에서 일일히 파일 경로를 접근하는 것이 아닌 아래와 같은 방법으로 기본포트로만 접근하여 원하는 html 파일이 보이기 해줄 수 있다.
    
    - autoUpload.sh
    
```sh
  #!/bin/bash

  if [ $# -eq 1 ]; then
    cntxt=$1
    echo $cntxt
    sed -i '$ d' tuneindex.sh
    echo "cat /usr/share/nginx/html${cntxt} > /usr/share/nginx/html/index.html" >> tuneindex.sh
  fi

  msg=$(date +"%Y-%m-%d %T")" content edit"

  git add . && git commit -m " $msg " && git push origin master
  ```
      - Dockerfile
      
  ```docker
  FROM nginx
  ADD ./ /usr/share/nginx/html
  RUN chmod +x /usr/share/nginx/html/tuneindex.sh
  RUN /usr/share/nginx/html/tuneindex.sh
  EXPOSE 80
  ```
      
      ⚠️ * tuneindex.sh 파일을 처음 만들 때 #!/bin/bash 의 명시와 다음줄에 임의의 더미 명령어를 임시로 만들어줘야한다. *
      - 사용법은 autoUpload.sh 실행시 인자값으로 "/[경로].html" 을 넘겨주면 동작한다.

## ISSUE 
  - jenkins가 설치된 server에서 Execute Shell 실행시, jenkins에 대한 sudo 명령어 사용권한을 따로 추가해줘야 한다.
   : https://hyunmin1906.tistory.com/282
  
  - Docker Hub에 Push 하는 과정에서 오류가 난다면 $ sudo docker login 명령을 통해 사용하는 레포지토리 소유자의 ID로 로그인이 잘 되어 있는지 확인 해줘야한다.

