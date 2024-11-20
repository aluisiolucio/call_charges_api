# Call Charges API

Uma API desenvolvida em `Python/FastAPI` para gerenciar registros de chamadas telefônicas detalhadas e calcular contas mensais de um número de telefone específico. Este projeto foi implementado como parte de um teste técnico de backend.

## 📋 Especificações

Esta API atende aos seguintes requisitos principais:

1. **Receber registros detalhados de chamadas**:
   - Tipos de registros: início e fim de chamadas.
   - Campos do registro:
     - `id`: Identificador único.
     - `type`: Tipo do registro (`start` ou `end`).
     - `timestamp`: Data e hora do evento.
     - `call_id`: Identificador único da chamada.
     - `source`: Número de origem (apenas para registros de início).
     - `destination`: Número de destino (apenas para registros de início).

2. **Obter conta telefônica**:
   - Entradas:
     - Número de telefone (obrigatório).
     - Período de referência no formato `MM/AAAA` (opcional; padrão é o último mês fechado).
   - Saída:
     - Informações do assinante, período e registros de chamadas detalhados.

3. **Regras de precificação**:
   - **Horário padrão (06:00 às 22:00)**:
     - Taxa fixa: R$ 0,36.
     - Taxa por minuto: R$ 0,09 (cobrada por minuto completo).
   - **Horário reduzido (22:00 às 06:00)**:
     - Taxa fixa: R$ 0,36.
     - Sem cobrança por minuto.

## 🚀 Tecnologias Utilizadas

- **Python 3.12+**
- **FastAPI** para criação da API.
- **PostgreSQL** como banco principal.
- **Alembic** para controle de versões do banco de dados.
- **Docker e Docker Compose** para configuração do ambiente.
- **Pytest** para testes.
- **Poetry** para gerenciamento de dependências.

## 🛠️ Instalação e Configuração

1. **Clone o Repositório**

   ```bash
   git clone https://github.com/aluisiolucio/call_charges_api.git
   cd call_charges_api
   ```

2. **Configuração de Ambiente**

   Copie o arquivo `.env.example` para `.env` e configure as variáveis:

   ```env
    DATABASE_URL=postgresql+psycopg://<user>:<password>@<host>:<port>/<dbname>
    DB_USER=<user>
    DB_PASSWORD=<password>
    DB_NAME=<dbname>
    SECRET_KEY=<sua-chave-secreta>
    ALGORITHM=<Algoritmo para JWT>
    ACCESS_TOKEN_EXPIRE_MINUTES=<Tempo para expiração do token>
   ```

3. **Execução com Docker**

   Certifique-se de ter **Docker** e **Docker Compose** instalados.

   ```bash
   docker compose up --build
   ```

   Isso iniciará os serviços da API e do banco de dados.

## 🔍 Documentação da API

### Principais Endpoints

1. **Registrar chamadas**
   - **PUT /api/v1/call_records**
   - Entrada: JSON com os dados da chamada.

2. **Consultar conta telefônica**
   - **GET /api/v1/phone_bill**
   - Parâmetros:
     - `phone_number`: Número do telefone.
     - `period`: Período de referência no formato `MM/AAAA`.

3. **Autenticação**
   - **POST /api/v1/auth/sign_up**: Criação de usuário.
   - **POST /api/v1/auth/sign_in**: Login.
   - **POST /api/v1/auth/refresh_token**: Renovação do token.

## 🌐 Deploy com CI/CD no Fly.io

Este projeto está configurado para **Continuous Integration (CI)** e **Continuous Deployment (CD)**, utilizando Github Actions e Fly.io como ambiente de produção.

### Configurações do Fly.io

- **Aplicação**: `call-charges-api`
- **Região primária**: `gru` (São Paulo, Brasil)
- **Configuração da Máquina Virtual**:
  - Tamanho: `shared-cpu-1x`
  - Memória: `256MB`

Com essa configuração, o ambiente de produção é eficiente e econômico, inicializando sob demanda e garantindo alta disponibilidade.

### Acesso à API em Produção

A documentação interativa está acessível via Swagger UI em: [Swagger Call Charges API](https://call-charges-api.fly.dev/docs).

## 🧪 Testes

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
    poetry run task test
    ```

    Isso executará todos os testes dentro da pasta `tests/` e exibirá o resultado no terminal.

## 🌐 Ambiente de Trabalho

- **SO**: Linux Ubuntu 24.04 LTS.
- **Editor/IDE**: VSCode.
- **Hardware**: Ryzen 5 5600, 32GB RAM.

## 🤝 Contribuição

Contribuições são bem-vindas! Se você deseja colaborar com este projeto, siga os passos abaixo:

1. **Faça um Fork do Repositório**  
   Crie uma cópia do projeto no seu GitHub utilizando o botão "Fork".

2. **Clone o Repositório Forkado**

   ```bash
   git clone https://github.com/seu-usuario/call_charges_api.git
   cd call_charges_api
   ```

3. **Crie uma Branch para suas Alterações**

   ```bash
   git checkout -b feature/sua-funcionalidade
   ```

4. **Implemente as Alterações**  
   Faça suas alterações no código, seguindo as melhores práticas e garantindo que os testes passem.

5. **Execute os Testes**

   ```bash
   poetry run task test
   ```

6. **Faça o Commit das Alterações**

   ```bash
   git commit -m "feat: descrição da sua funcionalidade"
   ```

7. **Envie suas Alterações para o Repositório Remoto**

   ```bash
   git push origin feature/sua-funcionalidade
   ```

8. **Abra um Pull Request (PR)**  
   Envie suas alterações para o repositório original e descreva suas contribuições no PR.

9. **Aguarde a Revisão**  
   Um dos mantenedores do projeto analisará suas alterações e dará um retorno.

## ⚖️ Licença

Distribuído sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.