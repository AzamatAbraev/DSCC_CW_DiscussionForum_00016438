# Discussion Forum Project | DSCC Coursework
**Student ID:** 00016438
**Module:** Distributed Systems and Cloud Computing (WIUT)

## Project Deliverables
* **Live Application:** [https://dscc-cw-00016438.uaenorth.cloudapp.azure.com/](https://dscc-cw-00016438.uaenorth.cloudapp.azure.com/)
* **GitHub Repository:** [https://github.com/AzamatAbraev/DSCC_CW_DiscussionForum_00016438.git](https://github.com/AzamatAbraev/DSCC_CW_DiscussionForum_00016438.git)
* **Docker Hub:** [https://hub.docker.com/r/biotechchy/dscc-cw-app](https://hub.docker.com/r/biotechchy/dscc-cw-app)
* **Video Demonstration:** [https://drive.google.com/file/d/1V4yo_cYXc3LED9egIvrgnagJvuF5dhau/view?usp=sharing](https://drive.google.com/file/d/1V4yo_cYXc3LED9egIvrgnagJvuF5dhau/view?usp=sharing)
* **Test Credentials:** Admin: `00016438` | Password: `00016438`

## Project Description
This project is a Django web application developed for the **Distributed Systems and Cloud Computing (DSCC)** module.

## Features
* **User Authentication**: Secure registration, login, and logout functionality.
* **Discussion Management**: Full CRUD operations (Create, Read, Update, Delete) for forum posts.
* **Search**: Search posts by description or title
* **Upvote**: Upvote (can be taken back) specific post
* **Relational Database**: PostgreSQL database with a number of many-to-one and many-to-many relationships.
* **Admin Interface**: Django Admin panel for content moderation.
* **Production Ready**: Gunicorn and Nginx with HTTPS enforcement.


## Technologies Used
* **Backend**: Django 5.2.11, Python 3.12.3, gunicorn 21.0.0(available in requirements.txt)
* **Database**: PostgreSQL
* **Web Server**: Nginx (Reverse Proxy) & Gunicorn (WSGI)
* **Containerization**: Docker (Multi-stage builds) & Docker Compose
* **CI/CD**: GitHub Actions
* **Cloud Hosting**: Azure VM - Ubuntu 24.04 LTS
* **DNS**: Azure domain
* **SSL/TLS**: Let's Encrypt (Certbot)
* **Security**: UFW Firewall, and Non-root Docker users


## Local Setup Instructions
To run this project on your local machine:

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/AzamatAbraev/DSCC_CW_DiscussionForum_00016438.git
    cd DSCC_CW_DiscussionForum_00016438
    ```
2.  **Environment Setup**:
    Create a `.env` file in the root directory based on the documentation below.
3.  **Run with Docker**:
    ```bash
    sudo docker compose up --build
    ```

4.  **Create a superuser for admin access**:
    ```bash
    sudo docker compose exec web python manage.py createsuperuser
    ```

5.  **Access the App**:
    The application will be available at `http://localhost:8000`.


## Environment Variables Documentation
The following variables are required for the application to function correctly in both development and production environments. You should include the following in .env file before running docker commands:

| Variable | Description |
| :--- | :--- |
| `SECRET_KEY` | Unique key for Django cryptographic signing. |
| `DEBUG` | Set to `False` in production. |
| `ALLOWED_HOSTS` | Comma-separated list of host/domain names. |
| `POSTGRES_DB` | Name of the PostgreSQL database. |
| `POSTGRES_USER` | Database username. |
| `POSTGRES_PASSWORD` | Database password. |
| `POSTGRES_HOST` | Database service name `db`. |
| `POSTGRES_PORT` | 5432 |

## 🌐 Deployment & CI/CD Pipeline
The deployment is fully automated via GitHub Actions (`.github/workflows/deploy.yml`).

### Pipeline Workflow:
* **Code Quality**: Executes `flake8` for linting (some features are disabled)
* **Testing**: Runs a suite of `pytest-django` tests and 2 sanity tests
* **Containerization**: 
  * Builds an optimized Docker image (Multi-stage, < 200MB).
  * Pushes the image to **Docker Hub**.
* **Production Release**: 
  * Connects to the Azure VM via SSH.
  * Pulls the latest image and performs a rolling restart.
  * Automated execution of `migrate` and `collectstatic`.