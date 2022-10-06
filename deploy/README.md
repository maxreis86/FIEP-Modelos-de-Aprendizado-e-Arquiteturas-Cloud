## Deploy usando Serverless e AWS Cloudformation
1. Colar o conteúdo da função def lambda_handler no arquivo handler.py
2. Remover o prefix ./output_model/models/best/ que aparece duas vezes no código handler.py
3. Confirmar se todas as bibliotecas com import no código handler.py foram incluídas no arquivo requirements.txt (OBS: Sempre inclua a versão da biblioteca para evitar que seu código pare de funcionar quando uma nova versão for publicada)
4. Altere o nome "StackedEnsemble_BestOfFamily_4_AutoML_1_20221006_02202.zip" para o nome do melhor modelo no arquivo Dockerfile
5. Conferir todas as configurações do arquivo serverless.yml, principalmente o parâmetro "querystrings" onde você deve informar todos os campos que serão obrigatórios na chamada da API