# Orquestração com Docker e Autenticação OAuth2 – FESF-SUS (Item 02)

Este repositório contém a entrega exclusiva do **Item 02** do Barema de Seleção Técnica da FESF-SUS. O objetivo deste módulo é comprovar a conteinerização funcional da API Backend e a implementação de um fluxo seguro de autenticação utilizando o protocolo **OAuth2 (Bearer Tokens)**.

---

## 🚀 Tecnologias e Padrões Aplicados

* **Docker:** Criação de uma imagem customizada, segura e otimizada para o ecossistema Python.
* **Docker Compose:** Orquestração de serviços de forma unificada, estabelecendo redes isoladas (`fesf_network`) e volumes para persistência de dados.
* **FastAPI (OAuth2PasswordBearer):** Utilização do fluxo nativo do framework para segurança de endpoints, geração e validação de tokens de acesso.
* **Builds Multi-estágio:** Técnica aplicada no `Dockerfile` para garantir que a imagem final contenha apenas o estritamente necessário para a execução, reduzindo a superfície de vulnerabilidades.

---

## 🛡️ Implementação do OAuth2 (Segurança)

A API backend foi blindada seguindo os padrões rigorosos de segurança de dados:
1.  **Endpoint `/token`:** Recebe as credenciais (`username` e `password`) via formulário seguro `x-www-form-urlencoded`, valida no banco de dados e retorna um Token Bearer de acesso.
2.  **Controle de Acesso Baseado em Papéis (RBAC):** Os middlewares e dependências do FastAPI injetam o usuário atual (`get_current_user`) e barram requisições não autorizadas usando o escopo do protocolo OAuth2.
3.  **Segredos e Chaves:** Configuração preparada para receber chaves de assinatura assimétrica por meio de variáveis de ambiente do contêiner (`SECRET_KEY`).

---

## 🗂️ Estrutura do Repositório

```text
├── Dockerfile             # Script de build multi-estágio da API Python
├── docker-compose.yml     # Maestro da infraestrutura (API + Banco + Rede)
├── main.py                # Código principal com os endpoints e regras OAuth2
├── schemas.py             # Modelagem de dados limpa via Pydantic
├── requirements.txt       # Dependências do projeto Python
└── README.md              # Documentação técnica do item
