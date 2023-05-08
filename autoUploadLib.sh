#!/usr/bin/expect -f

set ip "192.168.108.199"
set user "root"
set password "test123"

spawn ssh $user@$ip "java -jar jenkins-cli.jar -s http://192.168.108.199:8080/ -auth @.jenkins-cli build WebStudyAtMetanet -s -v"

expect {
    "*(yes/no)?*" {
        send "yes\r"
        exp_continue
    }
    "*assword:*" {
        send "$password\r"
    }
}

interact