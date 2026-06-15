# Arena Games - Sistema de Gerenciamento 

**Disciplina:** LPOO 2026-1  
**Curso:** Ciência da Computação - IFSul, Câmpus Passo Fundo  
**Aluno:** Rodrigo Pereira Barbosa  
**Professora:** Vanessa Lago Machado  


## Descrição do Projeto

O **Arena Games** é um sistema completo de gerenciamento de torneios de e-sports desenvolvido em Python. Utilizando uma interface gráfica amigável desenvolvida com a biblioteca Tkinter e garantindo a persistência de dados robusta por meio de um banco de dados PostgreSQL. O sistema foi projetado para administrar desde o cadastro de jogos e participantes (equipes e jogadores) até a criação de torneios com diferentes formatos, incluindo inscrições, chaveamento automático e registro de resultados de partidas.

Este projeto foi desenvolvido como requisito avaliativo da disciplina de Linguagem de Programação Orientada a Objetos (LPOO), integrando os conhecimentos práticos da academia com arquiteturas reais.

---

## Estrutura do Projeto e Módulos

O repositório está rigidamente estruturado para separar as responsabilidades seguindo o padrão de arquitetura **MVC (Model-View-Controller)** em conjunto com **DAO (Data Access Object)**:

- 📂 `model/`: Contém as classes de domínio do negócio, representando as entidades puras e suas relações.
- 📂 `dao/`: Abriga as classes responsáveis exclusivamente pela persistência e comunicação direta com o banco de dados PostgreSQL.
- 📂 `controller/`: Intermediários de fluxo; conectam a interface gráfica (`View`) às regras de negócio e ao acesso a dados (`DAO`/`Model`).
- 📂 `view/`: Contém os componentes de interface de usuário elaborados com Tkinter.
- 📂 `sql/`: Scripts de banco de dados, DDLs e DMLs de estruturação inicial.
- 📂 `assets/`: Recursos gráficos, como ícones e imagens.
- 📄 `main.py`: Ponto de entrada (entrypoint) que inicializa e orquestra a aplicação.

---

## Requisitos do Projeto

### 1. Classes de Domínio e Persistência (Mínimo de 3)
O sistema modela perfeitamente múltiplas entidades orientadas a objetos, sendo as principais com mapeamento completo no banco:
1. **Jogo**
2. **Equipe**
3. **Jogador**

### 2. CRUD Completo na Interface Gráfica
Na interface em Tkinter (no módulo `view/`), foram implementadas janelas que permitem realizar **100% das operações CRUD (Create, Read, Update, Delete)** para pelo menos duas entidades vitais do escopo:
-  **Jogadores** (Inclusão, Listagem, Edição de perfil e Remoção)
-  **Equipes** (Criação de time, Visualização dos membros, Edição de nome/logo e Desativação)

### 3. Padrões de Projeto Aplicados
Além de demonstrar os pilares da POO (Encapsulamento, Herança e Polimorfismo), a arquitetura conta com a aplicação sólida de pelo menos 2 Padrões de Projeto (Design Patterns):
1. **DAO (Data Access Object) [Obrigatório]:** Centraliza toda a execução de queries ao banco de dados e isola a base de dados do restante do código, garantindo segurança e coesão.
2. **MVC (Model-View-Controller) [Adicional]:** Divide de maneira estrutural a apresentação da camada de dados e de controle de estado do aplicativo.

---

## Diagrama de Classes de Dominio

O projeto conta com um diagrama que explica a herança, agregação e multiplicidade entre as entidades (ex: 1 Equipe contém N Jogadores, 1 Torneio abrange N Equipes).

> **[Clique aqui para visualizar o Diagrama de Classes de Domínio completo](./assets/classes_dominio.png)**

## Diagrama de Casos de uso

> **[Clique aqui para visualizar o Diagrama de Classes de Casos de Uso](./assets/diagrama_casos_uso.png)**

## Factory

> **[Clique aqui para visualizar o Diagrama Factory completo](./assets/factory.png)**

## Factory

> **[Clique aqui para visualizar os Relacionamentos completo](./assets/relacionamentos.png)**
---

## Declaração de Uso de IA

**Ferramenta utilizada:** Amazon Q  
**Propósito:** A inteligência artificial Amazon Q foi utilizada como assistente de codificação e produtividade durante o desenvolvimento deste projeto. Ela auxiliou na estruturação inicial das classes do padrão DAO, na geração de trechos de código estruturais para a interface gráfica em Tkinter e na revisão da documentação, apoiando o objetivo contínuo de alcançar métricas de qualidade de um desenvolvedor pleno.

---

### Pré-requisitos
- **Python 3.10 ou superior**.
- **PostgreSQL** instalado.
- Biblioteca `psycopg2` ou similar para o banco de dados.

