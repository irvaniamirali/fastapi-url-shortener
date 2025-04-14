# FastAPI URL Shortener

A high-performance, asynchronous URL shortening service built with **FastAPI** and **Tortoise ORM**.  
It features user authentication, rate-limiting using the **Token Bucket Algorithm**, clean modular architecture, and logging middleware.

---

## Features

- JWT Authentication
- Token Bucket Rate Limiting
- URL Shortening and Redirection
- Async Testing with `pytest`
- Dockerized for Deployment
- Rotating Log File Support
- Modular Project Structure

---

## API Endpoints

### Authentication

- `POST /token` — Get JWT access token

### User Routes

- `POST /users/` — Register a new user
- `GET /users/me` — Get current user info

### URL Routes

- `POST /urls/` — Create short URL
- `GET /urls/` — Get user's URLs
- `GET /urls/{short_url}` — Get details of a short URL
- `DELETE /urls/{short_url}` — Delete a short URL

### Redirection

- `GET /{short_url}` — Redirect to original URL

---

## Token Bucket Algorithm

The **Token Bucket** algorithm is used for rate-limiting requests per user.  
Each user is assigned a virtual “bucket” that fills at a steady rate (tokens per second).  
Requests consume tokens — if no tokens are available, the request is blocked or delayed.

This technique allows:
- Short bursts of traffic
- Controlled long-term request rate
- Fair usage among users

Implementation is in: `app/middleware/token_bucket_limiter.py`

---

## Setup

### Cloning the Project

To get started with the project, first clone the repository to your local machine using Git:

```shell
git clone https://github.com/irvaniamirali/fastapi-url-shortener.git
cd fastapi-url-shortener
```

### Installation Dependencies

To install the project dependencies, make sure you have pip and Python 3.x installed on your system. Then run the following command in your terminal:

```shell
pip install -r requirements.txt
```

### Environment Variables Setup

To run the project, you need to set up your environment variables. Follow these steps:
Copy the .env.sample file to create a new file named .env in the root directory of the project:

```shell
cp .env.sample .env
```
Open the newly created .env file in a text editor and update the values according to your configuration.

### Running the Application Locally
To run the application locally, use the following command:

```shell
uvicorn main:app --reload
```
In this command, main is the name of your Python file (without the .py extension) containing the FastAPI app, and app is the instance of FastAPI in that file. After this command, the application will be accessible at http://127.0.0.1:8000.


## Contributing
If you would like to contribute to this project, please create an issue or submit a pull request.

## License
This project is licensed under the Apache License.