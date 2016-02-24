#Overview

1. O serviço rest utiliza como container Docker Generic e execução automática com Dockerfile com expose na porta 8000.
2. O projeto utiliza como banco PostgreSQL pelo RDS do AWS.
3. Além disso, é necessário criar a instância no AWS Elastic BeanStalk (com docker generic).
4. Para facilitar a utilização das keys de acesso ao database, adicione os environment variables do banco durante os passos de criação da instância.

## RDS DashBoard

1. Clique em Launch

## Configurando com Elastic BeanStalk

1. Acesse o Elastic BeanStalk pelo painel do AWS
2. Clique no botão "Actions" no lado direito
3. E depois em "Launch New Environment"
4. Clique em "Create web server"
5. Em "Select a plataform", selecione "Generic Docker" e depois Next
6. Selecione a opção "Upload your own", e envie o arquivo docker.zip dentro da pasta "docker" do projeto
7. Clique em Next
8. Renome o Environment para o nome que chamar melhor (meu caso será: shortcutElastic) e clique Next
9. Clique Next (já temos no RDS e VPC)
10. Selecione a sua EC2 key pair que chamar util.
11. Clique Next
12. Agora, adicione as informações para acesso ao Postgres:
> DATABASE_NAME NOME_DO_DB
> DATABASE_USERNAME USERNAME
> DATABASE_PASSWORD PASSWORD
> DATABASE_HOST ENDPOINT_DO_RDS
13. Clique Next
14. Clique Launch

# API - GET POST DELETE

- IP_ADDRESS/api/users/ (GET) Lista todos os usuários com suas respectivas URLs (para testes)
- IP_ADDRESS/api/user/ (POST) id=chaordic Cria um usuário no db
- IP_ADDRESS/api/user/:USER_ID (GET/DELETE) Obtem um usuário com suas URLs ou deleta
- IP_ADDRESS/api/users/:USER_ID/urls/ (POST) Cria uma URL para o usuário e retorna dados sobre ela
- IP_ADDRESS/api/url/:URL_ID (DELETE/REDIRECT) Redireciona uma URL ou deleta
- IP_ADDRESS/api/url/:SHORT_URL (REDIRECT) Rediciona uma URL
- IP_ADDRESS/api/stats/:URL_ID (GET) Retorna estatistica da URL
- IP_ADDRESS/api/user/:USER_ID/stats/ (GET) Retorna estatisticas das URLs de um usuário
- IP_ADDRESS/api/stats/ (GET) Retorna estatisticas globais