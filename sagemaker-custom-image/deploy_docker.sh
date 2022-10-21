aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 702113447940.dkr.ecr.us-east-1.amazonaws.com
docker build -t aula-deploy-modelos .
docker tag aula-deploy-modelos:latest 702113447940.dkr.ecr.us-east-1.amazonaws.com/aula-deploy-modelos:latest
docker push 702113447940.dkr.ecr.us-east-1.amazonaws.com/aula-deploy-modelos:latest