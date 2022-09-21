# FIEP-Modelos-de-Aprendizado-e-Arquiteturas-Cloud

### Bootcamp 3 (Sistemas Inteligentes) do curso de Pós-Graduação em Engenharia de Dados e Inteligência Artificial nas Faculdades da Industria

Ao final de curso você estará apto(a) a desenvolver e implementar um modelo de Machine Learning usando as ferramentas disponíveis na AWS. Vamos começar 🚀


## Criar uma conta na AWS

1. Use esse link para criar sua conta e incluir um método de pagamento
[aws.amazon.com/free](aws.amazon.com/free)
2. Ao logar na conta da Amazon clique no nome do seu usuário no canto superior direito e depois em configurações (Settings)
3. Em Localização e região padrão (Localization and default Region) clique em editar e defina *Language: English (US)* e *Default Region: US East (N. Virginia) us-east-1*

## Amazon S3 (Simple Storage Service)
1. Em *Services*, no canto superior esquerdo procure por *S3*
2. Clique em *Create bucket* no canto superior direito
3. Defina *Bucket name*: **aula-deploy-modelos**
4. Deixe todas as outras configurações com o padrão
5. Clique em *Create bucket* no canto inferior direito

## Amazon ECR (Elastic Container Registry)
1. Em *Services*, no canto superior esquerdo procure por *Elastic Container Registry*
2. Em *Create a repository* clique em *Get Started* e defina os parâmetros abaixo:
3. Visibility settings: Private
4. Repository name: aula-deploy-modelos
5. Deixe todas as outras configurações com o padrão
6. Clique em *Create repository*
7. Clique no nome do repositório que acabou de ser criado em *Repository name*
8. Clique em *View push commands*
9. Deixe a aba *macOS / Linux* aberta, pois os comando 1 ao 4 serão usado no próximo passo: Cloud9

## Amazon Cloud9
1. Em *Services*, no canto superior esquerdo procure por *Cloud9*
2. Clique em *Create environment* no canto superior direito
3. Defina *Name: aula-deploy-modelos*, *Description : aula-deploy-modelos* 
4. Clique em **Next Step** e defina todos os parâmetros abaixo
5. Environment type: Create a new EC2 instance for environment (direct access)
6. Instance type: m5.large (8 GiB RAM + 2 vCPU)
7. Platform: Amazon Linux 2 (recommended)
8. Cost-saving setting: After 30 minutes (default)
9. Network settings (advanced)
10. Network (VPC): default
11. Subnet: us-east-1c
12. Clique em **Next Step** e **Create environment**
13. Clonar o repositório do git digitando a linha de comando abaixo no terminal  do Cloud9 (ec2-user:~/environment $): *git clone https://github.com/maxreis86/FIEP-Modelos-de-Aprendizado-e-Arquiteturas-Cloud.git*
14. Entrar na pasta da aula usando o comando: *cd FIEP-Modelos-de-Aprendizado-e-Arquiteturas-Cloud/sagemaker-custom-image*
15. Precisamos aumentar o espaço em disco dessa máquina virtual usando o comando: *bash resize.sh*
16. Executar os comandos 1 ao 4 conforme orientação da página *Push commands for aula-deploy-modelos* visto anteriormente:
17. *aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 702113447940.dkr.ecr.us-east-1.amazonaws.com*
18. *docker build -t aula-deploy-modelos .*
19. *docker tag aula-deploy-modelos:latest 702113447940.dkr.ecr.us-east-1.amazonaws.com/aula-deploy-modelos:latest*
20. *docker push 702113447940.dkr.ecr.us-east-1.amazonaws.com/aula-deploy-modelos:latest*
21. Após criar a imagem usando Docker, desligue a instância do Cloud9 executando o comando: sudo shutdown
22. Feche o Cloud9

## Amazon SageMaker
1. Em *Services*, no canto superior esquerdo procure por *Amazon SageMaker*
2. Abrir > Images > Create image siga os próximos passos preenchendos todos os parâmeros abaixo
3. Em *Image source* copiar o *Image URI* da imagem aula-deploy-modelos criada no Elastic Container Registry clicando em *Copy URI*: 702113447940.dkr.ecr.us-east-1.amazonaws.com/aula-deploy-modelos:latest
4. Image name: aula-deploy-modelos
5. Image display name: aula-deploy-modelos
6. Description: aula-deploy-modelos
7. IAM role: Create a new role
8. S3 buckets you specify - optional: Any S3 bucket
9. Create role
10. Advanced configuration. User ID (UID) - optional: 0 e Group ID (GUID) - optional: 0
11. Image type: SageMaker Studio image
12. Submit
13. Control panel
14. Setup SageMaker Domain: Quick setup (1 min)
15. User profile > Name: aula-deploy-modelos
16. Default execution role: deixo o Default e clique em *Submit* e aguarde quando aparecer *Preparing SageMaker Domain*
17. Em *Amazon SageMaker > Control Panel > Images* clique em *Attach image* e siga os passos abaixo
18. Image source: Existing image
19. Select an existing image from the SageMaker Image store: aula-deploy-modelos
20. Available image versions: aula-deploy-modelos / Version 1
21. Clique em *Next*
22. Em Advanced configuration, preencha com 0 em *User ID (UID)* e *Group ID (GUID)*. (**Muito importante colocar *0* para evitar erro na hora de iniciar a instância no SageMaker**)
23. Image type: SageMaker Studio image
24. Preencher o *Kernel name* sem espaços: Python3
25. *Kernel display name - optional*: Python3
26. Deixa todas as outras opções como default e clique em *Submit*
27. Em *Amazon SageMaker > Control Panel > Users > aula-deploy-modelos clique em *Lounch App > Studio*
28. Após abrir o Amazon SageMaker Studio clique em *File > New > Terminal*
29. Clonar novamente o diretório do git com o comando no terminal na parte de baixo da tela (sagemaker-user@studio$): git clone https://github.com/maxreis86/FIEP-Modelos-de-Aprendizado-e-Arquiteturas-Cloud.git
30. Entrar na pasta da aula usando o comando: cd FIEP-Modelos-de-Aprendizado-e-Arquiteturas-Cloud
31. Criar uma branch com seu nome e sobrenome sem acento ou espaco usando: git checkout -b nome_sobrenome
32. Em *File Browser*, no canto superior esquerdo abra a pasta FIEP-Modelos-de-Aprendizado-e-Arquiteturas-Cloud
33. Abra o arquivo **1_Data_Prep.ipynb**
34. Vai aparecer a tela: Set up environment for "1_Data_Prep.ipynb". Selecione as opções abaixo
35. Image: Custom Image aula-deploy-modelos - v1
36. Kernel: Python3
37. Start-up script: No script
38. No canto superior direito clique em *Unknown*
39. Em Instance Type selecione: ml.t3.medium
40. Clique em *Save and continue*
41. Executar todos os códigos do notebook e seguir as instruções nos arquivos 1_Data_Prep.ipynb, 2_Fast_Machine_Learning.ipynb e 3_Explaining_Model.ipynb