## RAP: Research Article Repository

A *framework free* system that manages **dummy articles, their categories and authors**

---

## 📌 Summary
This project implements a repository for dummy articles
This was done with the intention to learn about servers hence no framework to handle server in the background

## ✅ Key Features

- Author Management (Create, Read, Update, or Delete Author)
- Category Management (Create, Read, Update, or Delete Category)
- Author Publisher (Create, Read, Update, or Delete Publisher)
- Articles Management (Create, Read, Update, or Delete Articles)


## 🛠️ Technology Stack

- Python 3.10+  
- Python standard library
- HTML5, CSS3, and JavaScript


## Prerequisites
- python3.10+

--------------------------


## 🚀 Setup Instructions

### sql files were given for DB initialization
###### real data and DB will be used in the future

### 1. Clone Repos

```bash
run - git clone https://github.com/thimmy962/RAP
```

### 2. - Change Directory into Repository
```bash
run - cd RAP
```

### 3. Migrate DB Schema to sqlite3 DB
```bash
run - sqlite3 db_name.sqlite3  // This opens a sqlite3 terminal
run - .read SQL/schema.sql
run - .read SQL/ initial_data.sql
run - .read SQL/article_data.sql
run - .exit // closes sqlite3 terminal
```

### 4. Run backend Engine
```bash
run - **python3 py_server/server.py backend_port_number** or ***py py_server/server2.py backend_port_number*
```

### 5. Run
```bash
run - **python3 -m http.server -d ./static frontend_port_number**
```




### run - python3 py_server/server or python3 py_server/server2.py

### The custom server for the html/css/js has not been written, you can use apache/nginx for now

--------------------------

## 📄 API Usage

Refer to the `api_references.md` file for complete documentation of the available endpoints.

--------------------------

## 📁 Project Structure

RAP/
├── py_server/
|    ├── server.py
|    ├── server2.py
|    ├── sock_views.py
|    └── views.py
├── static/
|    ├── page.css
|    ├── page.js
|    └──page.html
├── SQL/
|    ├── schema.sql
|    ├── initial_data.sql
|    └── article_data.sql
├── requirements.txt
├── README.md
└── .gitignore

--------------------------

## 📬 Contribution & Feedback

Feel free to fork this repository, submit issues, or open pull requests for improvements. Feedback is always welcome!
