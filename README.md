# ZipLink

ZipLink is a FastAPI-based URL shortener.

### Cloning the Project
To get started with the project, first clone the repository to your local machine using Git:

```shell
git clone https://github.com/irvaniamirali/zip-link.git
cd zip-link
```

### Installation Dependencies
To install the project dependencies, make sure you have pip and Python 3.x installed on your system. Then run the following command in your terminal:

```shell
pip install -r requirements.txt
```

### Environment Variables Setup
To run the project, you need to set up your environment variables. Follow these steps:

1. Copy the `.env.sample` file to create a new file named `.env` in the root directory of the project:
```bash
cp .env.sample .env
```
2. Open the newly created .env file in a text editor and update the values according to your configuration. 

### Running the Application Locally
To run the application locally, use the following command:

```shell
uvicorn main:app --reload
```

In this command, main is the name of your Python file (without the .py extension) containing the FastAPI app, and app is the instance of FastAPI in that file. After this command, the application will be accessible at http://127.0.0.1:8000.

### Routes Overview
#### Users
- POST `/api/users` Create User
- POST `/api/users/token` Login for Access Token
#### Urls
- GET `/api/urls`: Get URL details
- PUT `/api/urls`: Update URL details
- POST `/api/urls`: Create URL
- DELETE `/api/urls`: Delete URL
- GET `/api/urls/all`: Get all URLs of user
#### Redirect
- GET `/{key}`: Redirect to the target URL

### Contributing
If you would like to contribute to this project, please create an issue or submit a pull request.

### License
This project is licensed under the Apache License.
