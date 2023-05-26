
## 사설 레지스트리 구성

  - registry 이미지 pull
  ```sh
      sudo docker pull registry 
  ```
  - registry 5000 포트로 배포
  ```sh
      sudo docker container run -d --restart=always -p 5000:5000 -v /registry:/var/lib/registry/docker/registry/v2 --name registry registry:latest
  ```
  - private registry에 이미지 push (jenkins)
  ```sh
      sudo docker build --no-cache -t [IP주소]:5000/metabus:1.0 .
      sudo docker push [IP주소]:5000/metabus:1.0
  ```
  - test (저장된 image 확인)
  ```sh
      curl -X GET http://localhost:5000/v2/_catalog
  ```
      
  ⚠️. Docker 데몬 구성 파일을 편집합니다. 일반적으로 /etc/docker/daemon.json 파일을 편집합니다. 파일이 존재하지 않는 경우 새로 생성하십시오.
편집기를 사용하여 daemon.json 파일을 열고 다음과 같이 설정합니다.

  ```json
      {
        "insecure-registries": ["43.201.165.100:5000"]
      }
  ```

  0. CentOS의 8080(젠킨스 포트)와 앞으로 만들어질 임의의 컨테이너 포트포워딩 설정 (본인은 가상머신을 사용하여 호스트 OS의 내부포트와 연결시키줌)
  
  ```yml
      version: '3'
      services: 
        spring-app:
          container_name: metabus
          image: "localhost:5000/metabus:1.0"
          ports: 
            - "8080:8080"
        nginx: 
          container_name: nginx
          image: nginx
          ports:
            - "80:80"
          volumes: 
            - ./nginx2/conf.d:/etc/nginx/conf.d
          depends_on: 
            - spring-app 
  ```
