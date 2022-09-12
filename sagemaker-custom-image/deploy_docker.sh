aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 245799943033.dkr.ecr.us-east-1.amazonaws.com
docker build -t teste3 .
docker tag teste3:latest 245799943033.dkr.ecr.us-east-1.amazonaws.com/teste3:latest
docker push 245799943033.dkr.ecr.us-east-1.amazonaws.com/teste3:latest