## Overview

This project automates the migration of data from a MySQL relational database to a Neo4j graph database for the Faculty of Contemporary Sciences and Technologies at Tetovo. The migration aims to leverage Neo4j's graph capabilities to enhance data querying and relationship management.

## Features

- **Data Migration**: Transfer structured data from MySQL tables to Neo4j, preserving relationships and entities.
- **Data Transformation**: Convert relational schema entities (e.g., students, courses) into graph nodes and relationships.
- **Error Handling**: Robust error handling mechanisms to ensure data integrity during migration.
- **Performance Optimization**: Utilize Neo4j's efficient graph traversal for fast and complex query execution.

## Setup

- **Clone the repository**: ```git clone https://github.com/bahtibegum/NoSQL_Migration_Project.git```
- **Change directory**: ```cd NoSQL_Migration_Project```
- **Create a virtual environment**: ```python -m venv venv```
- **Enter the venv**: ```source venv/bin/activate``` (```venv\Scripts\activate.bat``` for Windows)
- **Install dependencies**: ```pip install -r requirements.txt```
- **Run script**: ```python unidb.py```

---

[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-312/)
[![Neo4j](https://img.shields.io/badge/Neo4j-4.4.7-green.svg)](https://neo4j.com/download/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)](https://dev.mysql.com/downloads/mysql/)
[![License](https://img.shields.io/badge/license-MIT-red.svg)](https://opensource.org/licenses/MIT)
