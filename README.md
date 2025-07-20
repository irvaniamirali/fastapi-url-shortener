# URL Shortener API with FastAPI

This project is a simple and fast URL shortener API built using FastAPI. It allows users to convert long URLs into short, memorable links and redirects them when the short link is accessed.

---

## Features

- **URL Shortening**: Convert long URLs into short, unique codes.

- **Redirection**: Redirect users from a short URL to its original long URL.

- **Fast & Efficient**: Built with FastAPI for high performance.

- **Database Integration**: Persistent storage for URL mappings.

- **Input Validation**: Ensures valid URLs are provided.

---

## Technologies Used

- Python 3.x

- FastAPI: Modern, fast (high-performance) web framework for building APIs.

- Uvicorn: ASGI server for running FastAPI applications.

- Pydantic: Data validation and settings management (used by FastAPI and for .env handling).

- [Your Chosen Database]: (e.g., SQLAlchemy for PostgreSQL/SQLite, Motor for MongoDB, etc.) - You'll need to specify your actual database here.

---

## Installation

### 1. Clone the repository:

```bash
git clone https://github.com/irvaniamirali/fastapi-url-shortener.git
cd fastapi-url-shortener
```

### 2. Create a virtual environment and activate it:
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

### 4. Environment Variables Setup:
To configure the application, you'll need to set up your environment variables.

Make a copy of the provided `.env.sample` file and rename it to `.env`:

```bash
cp .env.sample .env
```

Open the newly created `.env` file and update the variables according to your specific needs, such as your database connection string, application port, or any other sensitive configurations.

---

## Running the Application

To start the FastAPI application:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
This will run the application on http://localhost:8000. The --reload flag enables auto-reloading on code changes, which is great for development.

---

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

---

## License

This project is licensed under the Apache-2.0 License - see the LICENSE file for details.
 