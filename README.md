#End-to-End DevOps Automation Using Terraform, AWS, Docker, Jenkins & GitHub

# PROJECT GOAL
1.Create AWS infrastructure using Terraform
2.Deploy a Dockerized application
3.Automate deployment using Jenkins CI/CD
4.Use GitHub as source control
![project-workflow](images/1.png)

--------------------------------------------
# Inastall docker and git
`sudo apt update
`sudo apt install -y git docker.io`
___________________________________

## What is terrafrom ?
Terraform is a DevOps tool that allows you to create, manage, and update cloud infrastructure using code. Instead of manually setting up servers, databases, or networks, you define them in text files, and Terraform automatically provisions and manages them across multiple cloud providers, ensuring automation, consistency, and repeatability.

terafrom file extensio is "`.tf`"

# Step 1: How to install terrafrom 
#1:Add HashiCorp GPG key
This ensures that the packages are trusted and verified.
	
`wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg`

#2:Add HashiCorp repository
`echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(grep -oP '(?<=UBUNTU_CODENAME=).*' /etc/os-release || lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list`

#3:Update and install Terraform
`sudo apt update && sudo apt install terraform`

`terraform version`
________________________________________________

# step 2: AWS SETUP
1.Create AWS Account

2.Create IAM User
Programmatic access(Access via AWS CLI, SDK, API)
AdministratorAccess
 
![create_user](images/2.png)


---> configure AWS CLI <---
 `aws configure`
![create_user](images/3.png)
__________________________________

# step 3: create  require files and dirs
sudo mkdir devops-project
cd devops-project


![create file and dir require](images/4.png)

__________________________________

# Step 4: 
cofigure terrafrom files

--->
`sudo cd terraform`

--->
`sudo vim provider.tf`
provider "aws" {
  region = "us-east-1"
}

--->
`sudo vim variables.tf`
variable "instance_type" {
  default = "t2.micro"
}

variable "root_volume_size" {
  default = 20
}



--->
`sudo vim main.tf`

![configure_terrafom](images/5.png)

--->
`sudo vim main.tf`
resource "aws_security_group" "my_sg" {
  name = "web-sg"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "web" {
  ami                    = "ami-0c02fb55956c7d316"
  instance_type          = var.instance_type
  vpc_security_group_ids = [aws_security_group.my_sg.id]
  key_name               = "aws-key"
root_block_device {
  volume_size = var.root_volume_size
  volume_type = "gp3"
  delete_on_termination = true
}
  tags = {
    Name = "DevOps-EC2"
  }
}



after creting this you need to run these commands 


1.`terraform init`
![terraform-init](images/13.png)

2.`terraform plan`
![terraform-plan](images/14.png)

3.`terraform apply`
![terraform-apply](images/15.png)
![aws-ec2](images/16.png)

_____________________________

# step 4: creat app.py file and Docker file

![app.py Dockerfile](images/6.png)
![app.py ](images/7.png)
---->
`from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "DevOps Project Deployed Successfully!"

app.run(host="0.0.0.0", port=80)`
----->

`sudo vim Dockerfile'
![Dockerfile](images/8.png)
FROM python:3.9
WORKDIR /app
COPY app.py .
RUN pip install flask
CMD ["python", "app.py"]

##Test Docker Locally

`docker build -t devops-app .`
`docker run -d -p 80:80 devops-app`
#check from browser
http://localhost
______________________________

`sudo cd ..`
`sudo git init`
`sudo git add .`
`sudo git commit -m "Initial DevOps project"`
`sudo git branch -M main`
`sudo git remote add origin https://github.com/hasinUllah565/devops-project.git`
`git remote -v`
`sudo git push -u origin main`
![push-code-to-dockerhub](images/9.png)

![push-code-to-dockerhub](images/10.png)
_________________________________

# PART 5: JENKINS (CI/CD)
#connect your machine using ssh with your local
`ssh -i "jenkin1-key.pem" ubuntu@ec2IP`
![ssh-connect](images/17.png)

##Install Jenkins on EC2 or local VM

`sudo apt install -y openjdk-11-jdk`
`wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null
`
wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -`
`sudo apt update`

`sudo apt install jenkins -y`

![jenkins-installation](images/11.png)

##http://EC2-IP:8080

![welcom-jenkins](images/12.png)

#  Jenkinsfile (PIPELINE)
pipeline {
    agent any

    stages {
        stage('Clone Repo') {
            steps {
                git url: 'https://github.com/hasinUllah565/devops-project.git', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t devops-app app/'
            }
        }

        stage('Run Container') {
            steps {
                sh 'docker run -d -p 80:80 devops-app'
            }
        }
    }
}

_________________________________

Terraform creates AWS EC2
Jenkins pulls code from GitHub
Docker builds app
App runs on EC2
Website accessible via EC2 Public IP


________________________________________

Resume:

End-to-End DevOps Automation Project
• Automated AWS infrastructure provisioning using Terraform (EC2, Security Groups)
• Containerized a Python application using Docker
• Designed CI/CD pipeline using Jenkins integrated with GitHub
• Deployed Dockerized application on AWS EC2
• Used Infrastructure as Code (IaC) for scalable and repeatable deployments



