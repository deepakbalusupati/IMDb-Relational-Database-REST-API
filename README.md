# IMDb Relational Database & REST API

A scalable SQL database and RESTful API for movie information storage and retrieval, inspired by IMDb.

## Features

- RESTful API with Swagger documentation
- Web interface for browsing movies and actors
- MySQL relational database with optimized queries
- Pagination, search, and filtering
- User authentication (basic)
- Movie reviews and ratings

## Technologies

- Python
- Flask
- MySQL
- Flask-RESTful
- Bootstrap 5

## Setup

1. Clone the repository
2. Install MySQL and create a database
3. Run the schema and sample data scripts in `database/`
4. Create a `.env` file in the `config/` folder with your database credentials
5. Install Python dependencies: `pip install -r requirements.txt`
6. Run the application: `python app.py`

## API Documentation

After starting the application, access the Swagger UI at: `http://localhost:5000/api/docs`

## Project Structure