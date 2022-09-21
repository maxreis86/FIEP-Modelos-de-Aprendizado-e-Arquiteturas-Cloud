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
13. Clonar o repositório do git digitando a linha de comando abaixo no terminal  do Cloud9 (ec2-user:~/environment $): git clone https://github.com/maxreis86/FIEP-Modelos-de-Aprendizado-e-Arquiteturas-Cloud.git


para instalar node.js
https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/setting-up-node-on-ec2-instance.html