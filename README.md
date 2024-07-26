# Flask Questionnaire

A web application built using Python and Flask that allows users to register, log in, complete a questionnaire, and view their results. This application includes user authentication, data storage, and an admin panel for data export.

## Table of Contents

- [Project Overview](#project-overview)
- [Installation Instructions](#installation-instructions)
  - [Using Docker](#using-docker)
  - [Manual Installation](#manual-installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [Docker Image](#docker-image)
- [License](#license)


## Project Overview

The "Flask Questionnaire" project is a web application designed to collect user responses to a series of questions. Users can register, log in, complete the questionnaire, and view their results. Admin users can export the collected data for further analysis.

## Installation Instructions

### Using Docker

1. **Pull the Docker Image:**
   ```bash
   docker pull joeuzo/questionnaire:tagname
   ```

2. **Prepare the `.env` File:**
   Create a `.env` file in your working directory with the following content:
   ```makefile
   SECRET_KEY=your_secret_key
   DATABASE_URL=sqlite:///questionnaire.db  # Or your preferred database URL
   EMAIL_KEY=your_email_app_key
   EMAIL_ADDRESS=your_email@example.com
   ```

3. **Run the Docker Container:**
   ```bash
   docker run --env-file .env -p 5000:5000 joeuzo/questionnaire:tagname
   ```

### Manual Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/JoeUzo/Flask-User-Questionnaire.git
   cd Flask-User-Questionnaire
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Environment Variables:**
   Create a .env file in the root directory and add the following variables:
   ```makefile
   SECRET_KEY=your_secret_key
   DATABASE_URL=sqlite:///questionnaire.db  # Or your preferred database URL
   EMAIL_KEY=your_email_app_key
   EMAIL_ADDRESS=your_email@example.com
   ```

5. **Initialize the Database:**
   ```bash
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```

6. **Run the Application:**
   ```bash
   flask run
   ```

## Usage

Once the application is running, you can access it in your web browser at [http://127.0.0.1:5000/](http://127.0.0.1:5000/). Users can register, log in, complete the questionnaire, and view their results. Admin users (with user ID 1) have additional privileges, such as exporting data and managing the questionnaire.

## Features

- User Authentication (Registration, Login, Logout)
- Questionnaire with dynamic questions and scoring
- Age group selection
- Data storage and export functionality
- Admin panel for managing the application

## Contributing

Contributions are welcome! If you would like to contribute, please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Make your changes and commit them (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a new Pull Request

## Docker Image

You can find the Docker image for this project on Docker Hub:

[![Docker Image](https://img.shields.io/badge/Docker%20Hub-questionnaire--web-blue)](https://hub.docker.com/r/joeuzo/questionnaire)

To run the Docker image:

```sh
docker pull joeuzo/questionnaire:tagname
docker run --env-file .env -p 5000:5000 joeuzo/questionnaire:tagname
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
