# Call Charges API (Teste técnico backend)

Este projeto é uma API desenvolvida utilizando `Python/FastAPI` para receber registros detalhados de chamadas telefônicas e calcular as contas mensais para um número de telefone específico. A API foi implementada como um teste técnico para uma vaga de backend.

## Tecnologias utilizadas

- **Python** 3.12 ou superior
- **FastAPI** para criação da API
- **Poetry** para gerenciamento de dependências
- **Docker** e **Docker Compose** para execução do ambiente
- **Pytest** para executar os testes
- **Alembic** para migrations
- **SQLite** para executar nos testes
- **PostgreSQL** como banco principal

## Instalação e utilização

1. **Clone o repositório**

   ```bash
   git clone https://github.com/aluisiolucio/call_charges_api.git
   cd call_charges_api
   ```

2. **Configure as variáveis de ambiente presentes no arquivo `.env.example`**

    ```
    DATABASE_URL=
    DB_USER=
    DB_PASSWORD=
    DB_NAME=
    SECRET_KEY=
    ```
    Após configurar, renomeie o arquivo para `.env`

3. **Instale o Docker e Docker Compose**

    Caso ainda não tenha o Docker instalado, siga as instruções oficiais [aqui](https://docs.docker.com/get-started/get-docker/).

    Caso ainda não tenha o Docker Compose instalado, siga as instruções oficiais [aqui](https://docs.docker.com/compose/install/standalone/).

4. **Rodando o projeto com Docker Compose**

    Para rodar a aplicação usando Docker Compose, execute o seguinte comando:

    ```bash
    docker compose up --build
    ```

    Este comando irá configurar e iniciar os containers necessários para rodar a API e torná-la diponível para uso.

## Acessando a API

A API está diponível com uma interface interativa para testar os endpoints, utilizando o **Swagger UI**.

- Para acessar o Swagger, abra o navegador e vá até o endereço:  
  [Swagger Call Charges API](http://127.0.0.1:8000/docs)

O Swagger permite testar as rotas de maneira simples e visualizar todos os detalhes da API.

## Testes

Para executar os testes é necessário ter o Poetry instalado.

1. **Instale o Poetry**

   Caso ainda não tenha o Poetry instalado, siga as instruções oficiais [aqui](https://python-poetry.org/docs/#installation).

2. **Instale as dependências do projeto**

   Com o Poetry instalado, execute:

   ```bash
   poetry install
   ```

3. **Execute os testes**

    O projeto utiliza **pytest** para os testes. Para rodar os testes, utilize o seguinte comando:

    ```bash
    task test
    ```

    Isso executará todos os testes dentro da pasta `tests/` e exibirá o resultado no terminal.

## Funcionalidade

A API possui os seguintes endpoints:

- **PUT /api/v1/call_recors**: Grava/Atualiza os registros detalhados de chamadas de um número de telefone.
- **GET /api/v1/phone_bill**: Retorna a conta telefônica de um assinante
- **POST /api/v1/auth/sign_up**: Cria um usuário
- **POST /api/v1/auth/sign_in**: Autentica um usuário
- **POST /api/v1/auth/refresh_token**: Retorna o refresh_token

## Ambiente de trabalho

- **Editor/IDE:** VSCode
- **Máquina:**
    - SO: Linux Ubuntu 24.04 LTS
    - Processador: Ryzen 5 5600 (6/12)
    - Memória RAM: 32GB

## Contribuição

Contribuições são bem-vindas! Se você deseja melhorar o projeto, siga estes passos:

1. Fork o repositório.
2. Crie uma branch com a nova funcionalidade (`git checkout -b feature/nova-funcionalidade`).
3. Faça commit das alterações (`git commit -m 'Adicionei nova funcionalidade'`).
4. Envie para o repositório remoto (`git push origin feature/nova-funcionalidade`).
5. Abra um Pull Request.

## Licença

Este projeto é licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.