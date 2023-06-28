# Docs_metabus_porject

### CI/CD (jenkins)

```sh
# 빌드 전 캐시 데이터 삭제
sudo docker image prune
sudo docker system prune -a
sudo docker builder prune -a --force
# 빌드 시작 + push + ssh 접속 (.py)
sudo docker build -t 43.201.165.100:5000/metabus:1.0 .
sudo docker push 43.201.165.100:5000/metabus:1.0
sudo python3 /var/lib/jenkins/remotedeploy.py
```

### Slack notification setting

![image](https://github.com/bong44/metanetweb/assets/65393001/52dda10f-5244-412b-99aa-8bc84e4561b5)

### Remote ssh CD code

```python
import paramiko

def send_ssh_command(target_ip, target_username, target_private_key, command):
    # SSH 클라이언트 객체 생성
    ssh = paramiko.SSHClient()

    # 호스트 키를 신뢰할 수 있는지 확인하지 않음
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # 대상 EC2 인스턴스에 연결
        ssh.connect(target_ip, username=target_username, key_filename=target_private_key)

        # SSH 명령 실행
        stdin, stdout, stderr = ssh.exec_command(command)
        
        # 명령 실행 결과 출력
        print(stdout.read().decode())
        
        # 연결 종료
        ssh.close()
    except Exception as e:
        print(f"Error: {str(e)}")

# 대상 EC2 인스턴스의 IP 주소, 사용자 이름 및 개인 키 파일 경로 설정
target_ip = "ec2-43-201-165-100.ap-northeast-2.compute.amazonaws.com"
target_username = "ubuntu"
target_private_key = "/var/lib/jenkins/.ssh/jenkins-to-aws.pem"

# 실행할 SSH 명령 설정
command = "/home/ubuntu/dockerdeploy.sh"  # 예시로 'ls -l' 명령을 실행

# SSH 명령 전송
send_ssh_command(target_ip, target_username, target_private_key, command)


```
