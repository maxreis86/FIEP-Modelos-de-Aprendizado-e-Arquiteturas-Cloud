sudo dockerd
sudo aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 245799943033.dkr.ecr.us-east-1.amazonaws.com
sudo docker build -t teste2 .
sudo docker tag teste2:latest 245799943033.dkr.ecr.us-east-1.amazonaws.com/teste2:latest
sudo docker push 245799943033.dkr.ecr.us-east-1.amazonaws.com/teste2:latest