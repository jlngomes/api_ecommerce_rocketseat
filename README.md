# 🛒 E-commerce API - Flask

Este projeto é uma API robusta para gerenciamento de um e-commerce simplificado. O sistema permite o controle de usuários, catálogo de produtos e um fluxo completo de carrinho de compras.

---

## 🇧🇷 Português

### 🚀 Funcionalidades Principais

* **🔐 Autenticação e Segurança**: 
    * Sistema de sessões para garantir que apenas usuários autorizados realizem operações sensíveis.
    * Proteção de rotas administrativas e do carrinho, exigindo login ativo.
* **📦 Gestão de Catálogo (CRUD)**:
    * **Visualização**: Visitantes podem listar produtos e ver detalhes.
    * **Administração**: Usuários logados podem adicionar, atualizar e remover produtos da base de dados.
* **🛒 Fluxo de Compras**:
    * Carrinho personalizado vinculado à conta de cada usuário.
    * Gestão de itens (Adicionar/Remover) e simulação de **Checkout** (limpeza do carrinho após a compra).

### 🛠️ Tecnologias Utilizadas

* **Python / Flask**: Framework principal para construção da web API.
* **Flask-SQLAlchemy**: Manipulação do banco de dados de forma intuitiva (ORM).
* **Flask-Login**: Gestão de sessões e autenticação de utilizadores.
* **SQLite**: Banco de dados leve e eficiente para armazenamento local.
* **Flask-CORS**: Permite que a API seja acedida por diferentes interfaces (browsers ou Swagger).

### 📂 Estrutura do Banco de Dados

O sistema opera com três entidades principais:
1.  **Utilizador (`User`)**: Armazena nome de utilizador, senha e gere a relação com o carrinho.
2.  **Produto (`Product`)**: Armazena nome, preço e descrição técnica.
3.  **Item do Carrinho (`CartItem`)**: Tabela de ligação que associa produtos específicos a utilizadores.

### 📋 Como Testar (Portuguese)
1. **Iniciar a API**: 
   Execute o script principal para subir o servidor local:
   `python app.py`
2. **Login**: 
   Envie uma requisição `POST` para `/login` com as suas credenciais de usuário.
3. **Explorar**: 
   Acesse a rota `/api/products` para visualizar todos os itens disponíveis no catálogo.
4. **Comprar**: 
   Adicione os itens desejados ao carrinho e utilize a rota de `/checkout` para finalizar o pedido.

---

## 🇺🇸 English

### 🚀 Main Features

* **🔐 Authentication & Security**:
    * Session-based system to ensure only authorized users perform sensitive operations.
    * Route protection for administrative tasks and the shopping cart (requires active login).
* **📦 Catalog Management (CRUD)**:
    * **View**: Visitors can list products and see specific details.
    * **Management**: Logged-in users can add, update, and remove products from the database.
* **🛒 Shopping Workflow**:
    * Personalized shopping cart linked to each user account.
    * Item management (add/remove) and a **Checkout** simulation (clears the cart upon completion).

### 🛠️ Technologies Used

* **Python / Flask**: Main framework for the web API.
* **Flask-SQLAlchemy**: Intuitive database manipulation (ORM).
* **Flask-Login**: User session and authentication management.
* **SQLite**: Lightweight and efficient local database.
* **Flask-CORS**: Enables API access from different interfaces or browsers.

### 📂 Database Structure

The system operates with three main entities:
1.  **User (`User`)**: Stores username, password, and manages the cart relationship.
2.  **Product (`Product`)**: Stores name, price, and technical description.
3.  **Cart Item (`CartItem`)**: Linking table that associates specific products with users.

### 📋 How to Test (English)
1. **Start the API**: 
   Run the main script to start the local server:
   `python app.py`
2. **Login**: 
   Send a `POST` request to `/login` using your user credentials.
3. **Explore**: 
   Access the `/api/products` route to view all items available in the catalog.
4. **Buy**: 
   Add the desired items to your cart and use the `/checkout` route to complete your order.