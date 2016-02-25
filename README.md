#Overview

- O serviço rest utiliza como container Docker Generic e execução automática com Dockerfile com expose na porta 8000.
- O projeto utiliza como banco PostgreSQL pelo RDS do AWS.
- Além disso, é necessário criar a instância no AWS Elastic BeanStalk (com docker generic).
- Para facilitar a utilização das keys de acesso ao database, adicione os environment variables do banco durante os passos de criação da instância.

## Key Pair

1. Acesse EC2 no painel AWS
2. Clique em Key Pairs, depois em Create Key Pair
3. Adicione um rotulo para sua key, automaticamente vai salvar em seu pc.

## RDS DashBoard

1. Acesse RDS no painel AWS
2. Clique em Launch a DB Instance
3. Clique em PostgreSQL, e Select, e Next Step
4. Em DB Instance Class, selecione db.m1.small
5. Em Multi-AZ Deployment, selecione No
6. Em Storage Type, selecione Magnetic (mais barato)
7. Em Settings:
    7.1. DB Instance Identifier, coloque shortcut-instance-1 (somente exemplo)
    7.2. Master Username, coloque chaordicusername (somente exemplo)
    7.3. Master Password, coloque chaordicpassword (somente exemplo)
8. Selecione o VPC defaul (se quiser pode criar uma)
9. VPC Security Group: Selecione default (VPN) (caso não tenha uma) 
10. Em Database Options:
    9.1. Database Name, coloque shortcutdb
11. Clique em Launch DB Instance
12. Volte a Instance
13. Selecione a instancia que esta sendo criada
14. Clique no icone abaixo chamado Details
15. Procure por Security Groups e clique no link ao lado
16. Após a nova janela abrir, clique em Inbound no menu abaixo
17. Clique em Edit e adicione outro All Trafic, mas com Source para Anywhere (isso é somente para agilizar ok?)

## Configurando com Elastic BeanStalk

1. Acesse o Elastic BeanStalk pelo painel do AWS
2. Clique no botão "Actions" no lado direito
3. E depois em "Launch New Environment"
4. Clique em "Create web server"
5. Em "Select a plataform", selecione "Generic Docker" e depois Next
6. Selecione a opção "Upload your own", e envie o arquivo docker.zip dentro da pasta "docker" do projeto
7. Clique em Next
8. Renome o Environment para o nome que achar melhor (meu caso será: shortcutElastic) e clique Next
9. Clique Next (já temos no RDS e VPC)
10. Selecione a sua EC2 key criada anteriormente.
11. Clique Next -> Next -> Next -> Launch
15. Há possibilidade de dar timeout (error)
    15.1. Se isso acontecer, ainda no painel do Dashboard da sua Environment, acesse no menu do lado esquerdo a opção Configuration
    15.2. Clique em Updates and Deployments
    15.3. Altere o valor em Command timeout para 900
    15.4. Clique em Apply
    15.5. Espere terminar
16. Após terminar, ainda no painel de DashBoard, selecione a opção Configuration
    16.1. Clique em Software Configuration
    16.2. Agora, adicione as informações para acesso ao Postgres no Environment Properties utilizado pela aplicação:
    16.3. DATABASE_NAME shortcutdb
    16.4. DATABASE_USERNAME chaordicusername
    16.5. DATABASE_PASSWORD chaordicpassword
    16.6. DATABASE_HOST ENDPOINT_DO_RDS
        16.6.1. para o ENDPOINT_DO_RDS, abra uma nova aba no painel do AWS, acesse RDS, clique em Instances, selecione a instance do banco, e copiei o Endpoint SEM A PORTA
    16.7. Clique em Apply
16. Após finalizar, é so copiar o endereço do seu balance em:
    16.1. Acesse EC2 no painel do AWS
    16.2. Clique em Load Balancer
    16.3. Selecione o balancer na nossa instancia
    16.4. Copiei o DNS Name e cole em seu navegador
17. Utilize a API como quiser

## Ocean Digital - Para brincar

1. Crie um Droplet com a aplicação Docker
2. Acesse seu droplet
3. Baixe o arquivo docker.zip e descompacte
4. Execute: docker build .
5. Espere terminar
6. Execute: docker images
7. Copie o IMAGE ID da image que tem none na TAG e REPOSITORY
8. Execute após: docker run --name shortcut-django-app -p 8000:8000 -d COLE_AQUI
9. Execute: apt-get install nginx
10. Execute: mv nginx_master /etc/nginx/sites-enabled/default
11. Execute: service nginx restart
12. Copie o IP do seu droplet e abra em um navegador. Agora use a API

## API - GET POST DELETE

- IP_ADDRESS/api/users/ (GET) Lista todos os usuários com suas respectivas URLs (para testes)
- IP_ADDRESS/api/user/ (POST) id=chaordic Cria um usuário no db
- IP_ADDRESS/api/user/:USER_ID (GET/DELETE) Obtem um usuário com suas URLs ou deleta
- IP_ADDRESS/api/users/:USER_ID/urls/ (POST) Cria uma URL para o usuário e retorna dados sobre ela
- IP_ADDRESS/api/url/:URL_ID (DELETE/REDIRECT) Redireciona uma URL ou deleta
- IP_ADDRESS/api/url/:SHORT_URL (REDIRECT) Rediciona uma URL
- IP_ADDRESS/api/stats/:URL_ID (GET) Retorna estatistica da URL
- IP_ADDRESS/api/user/:USER_ID/stats/ (GET) Retorna estatisticas das URLs de um usuário
- IP_ADDRESS/api/stats/ (GET) Retorna estatisticas globais