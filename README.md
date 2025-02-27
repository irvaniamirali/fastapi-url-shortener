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

### Running the Application Locally
To run the application locally, use the following command:

```shell
uvicorn main:app --reload
```

In this command, main is the name of your Python file (without the .py extension) containing the FastAPI app, and app is the instance of FastAPI in that file. After this command, the application will be accessible at http://127.0.0.1:8000.

### Routes Overview
- POST `/api/admin`: Create Admin Key
- GET `/api/admin/url`: Get a URL details
- PUT `/api/admin/url`: Update a URL details
- POST `/api/admin/url`: Create a URL
- DELETE `/api/admin/url`: Delete a URL
- GET `/api/admin/urls`: Get all URLs
- GET `/{key}`: Redirect to the target URL

### Contributing
If you would like to contribute to this project, please create an issue or submit a pull request.

### License
This project is licensed under the Apache License.
