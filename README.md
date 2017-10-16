# Projeto: Challenge for developers

## Resumo

Este projeto foi desenvolvimento como base de teste de conhecimento para a empresa [Brainn.co](http://brainn.co/)

* [Instruções do solicitante](https://github.com/felipedecampos/challenge-for-developers#instruções-do-solicitante-brainnco)

### Pré-requisito

* [Python](https://www.python.org/downloads/) versão > 3. *
* [Git](https://desktop.github.com/)
* Virtualenv
```
$ pip install virtualenv
```
* Django
```
$ pip install django==1.11.6
```
* Behave
```
$ pip install behave
```

Verifique se tem todos os pré requisitos:
```
$ git --version
```
```
$ python3 -V
```
```
$ virtualenv env
```
```
$ python
>>> import django
>>> django.get_version()
```
```
$ python -m behave --version
```

### Instalação

Clone o repositório do projeto: 
```
$ git clone https://github.com/felipedecampos/challenge-for-developers.git
```
Instale todos os pacotes do arquivo: /python-django-skel/requirements.txt

Execute os seguintes comandos no terminal para instalar os pacotes:,

Linux:
```
$ pip3 install -r requirements.txt
```
Windows:
```
$ python -m pip install -U pip setuptools
```
```
$ python -m pip install matplotlib
```

Adicione seu TOKEN do GITHUB em uma variável de ambiente

Linux:
```
$ export GITHUB_API_TOKEN=SEU_TOKEN_GITHBUB
```
Windows:
```
$ set GITHUB_API_TOKEN=SEU_TOKEN_GITHBUB
```

## Rodar testes

Para rodar os testes de comportamento entre na pasta /tests/BDD
```
$ cd python-django-skel/core/tests/BDD
```
Verificando o ambiente
```
$ behave features/environment.feature
```

## Desenvolvido com:

* [Django](https://docs.djangoproject.com/en/1.11/) - The web framework used
* [Python](https://www.python.org/doc/) - Dependency Management

## Versionamento

Usado [Git](https://git-scm.com/doc) para versionamento. Para visualizar as versões disponíveis, veja [tags do repositório](https://github.com/felipedecampos/challenge-for-developers/tags).

## Autor

* **Felipe de Campos**
* [Site pessoal](http://site.felipedecampos.com.br) 
* [Github](https://github.com/felipedecampos)

## Licença

Este projeto não possui licença

# Instruções do solicitante (Brainn.co):

## Overview

O Github é uma rede social de programadores que possui uma funcionalidade interessante que permite curtir o repositório alheio. Trata-se de um botão escrito Star encontrado na página de cada repositório.  
Rick é um usuário ativo do Github que está sempre buscando novos projetos curtindo os que acha interessantes. Ele gostaria de poder adicionar um label ou tag para marcar o repositório de modo que ele possa filtrar. Por exemplo, ele encontrou um repositório chamado `react` e gostaria de adicionar as tags *javascript* e *frontend*.  
Como o Github não possui essa funcionalidade, Rick precisa de um sistema que consiga ajudá-lo com isso.

## Tecnologias

Na brainn.co não trabalhamos com uma linguagem ou framework apenas. Somos poliglotas e incentivamos o uso de novas tecnologias desde que o time concorde em conjunto e esteja preparado para assumir os riscos de ter que reimplementar utilizando alguma tecnologia mais tradicional em casos de incidentes.  
Entretanto, nesse momento, estamos com um time pequeno e por enquanto nossas opções de linguagem são limitadas.  
Escolha uma das linguagens abaixo para o desafio:

* Python
* Javascript
* Golang
* Java
* Ruby

## O que vai ser avaliado?

- Código limpo e coeso utilizando os princípios [SOLID](https://www.google.com.br/search?q=principios+solid&oq=principios+solid).
- API Restful utilizando Django, API Star, Flask ou Falcon
- Uso da API do Github
- Uso o ORM do Django ou SQLAlchemy para trabalhar com banco de dados
- Testes automatizados
- Cobertura de testes
- Linter do código
- Documentação da API utilizando API Blueprint, RAML ou Swagger)
- Conhecimento em Javascript, HTML e CSS
- Usabilidade

## Instruções

1. Faça um fork de repositório;
2. Descreva no `README.md` como configurar o projeto;
3. Envie por email a URL do fork.

## Desafio

O desafio é composto por 3 user stories:

### 1. Obter repositórios remotos e cadastrar no banco de dados local

> Como usuário, eu quero fornecer meu username e obter todos os repositórios que eu curti e salvar no banco de dados para depois conseguir adicionar minhas tags.

#### Cenário

O usuário executa algum comando ou script pelo terminal passando o username como parâmetro para que obtenha os repositórios do Github.

#### Critérios de Aceitação

* Deve obter os repositórios com star utilizando a API Rest v3 do Github. Utilizar a API v4 com GraphQL é um plus.
* O banco de dados pode ser SQLite3, MySQL ou Postgres.
* As informações que devem ser salvas no banco de dados são: ID do repositório, nome do repositório, url http e linguagem.

#### Exemplo de Uso

Dado o username gustavohenrique:

**API v3 via shell**

```sh
curl -slv https://api.github.com/users/gustavohenrique/starred?sort=updated&direction=desc
```

**API v4 via Python**
```python
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

user = 'gustavohenrique'
query = ''
  query {
  user(login: "%s") {
      starredRepositories(first: 1) {
        totalCount
        edges {
          node {
            id
            name
            url
            languages(first: 10) {
              edges {
                node {
                  name
                }
              }
            }
          }
          cursor
        }
        pageInfo {
          hasNextPage
          hasPreviousPage
          endCursor
        }
      }
  }'' % user
headers = {'Authorization': 'bearer %s' % os.getenv('GITHUB_API_TOKEN')}
url = 'https://api.github.com/graphql'
transport = RequestsHTTPTransport(url, headers=headers, use_json=True)
client = Client(transport=transport)
resp = client.execute(gql(query))
repositories = resp.get('user').get('starredRepositories')
print(repositories)
```

### 2. Adicionar tags para os repositórios

> Como usuário, eu quero poder adicionar tags (labels) para cada repositório para eu poder efetuar uma busca por tag.

#### Cenário

O usuário acessa o sistema pelo browser, visualiza a lista de repositórios cadastrados no banco de dados, seleciona um deles e consegue digitar tags separadas por vírgula para salvar em seguida.

#### Critérios de Aceitação

* O campo de tags no banco de dados pode ser um CharField comum, não precisa utilizar campos específicos do MySQL ou Postgres.
* Um repositório não pode ter tags duplicadas.
* Pode utilizar o Admin do Django se preferir.

### 3. Buscar repositórios por tag

> Como usuário, quero poder fornecer uma tag e obter os repositórios que possuem essa tag para visualizar na tela o resultado da minha busca.

#### Cenário

O usuário acessa o sistema pelo browser, digita uma tag e clica no botão. O sistema exibe todos os repositórios que tenham a tag definida.

#### Critérios de Aceitação

* Uma tela utilizando semantic-ui ou twitter bootstrap para aparência.
* Utilizar Ajax para obter os repositórios
* A busca não precisa estar perfeita. Se buscar pela tag `java` e retornar repositório contendo `javascript`, não tem problema.

## Considerações Finais

Entendemos as dificuldades do dia-a-dia para quem trabalha em ter que dedicar um tempo para resolver esse tipo de desafio. Por isso pedimos para que mesmo que você não consiga completar o desafio, nos envie assim mesmo. Não queremos julgar nossos candidatos, queremos apenas entender melhor a maneira como cada um pensa e age diante de um problema comum no mercado.  

Qualquer dúvida pode entrar em contato conosco.  

Boa sorte!!!