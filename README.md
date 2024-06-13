
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
