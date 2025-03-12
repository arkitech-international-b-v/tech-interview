# Tech Interview Arkitech

## Description

This is a mock project that uses some of the technologies used in Arkitech, but the main goal is to test your skills in the technologies you are familiar with.

The project contains a Python simulation script that publishes data to a MQTT broker, a FastAPI backend that consumes the data and stores it in a MongoDB database, and an Angular frontend that displays the data in a dashboard.

### Requirements: Tooling setup

Install the following tools to run this project for the interview:

- [Install Docker](https://www.docker.com/get-started/)
- [Install Python](https://www.python.org/downloads/)
- [Install UV tooling for Python](https://docs.astral.sh/uv/getting-started/installation/)
- [Install Node Version Manager - NVM to manage multiple versions of NodeJS](https://www.freecodecamp.org/news/node-version-manager-nvm-install-guide/)

## Backend setup
Path: `app`

### Instructions
How to run the Backend API in your local machine:

#### 1. Setup Docker
Go to the project folder and run docker build. This will create a MongoDB container and a simulator script publishing data to MQTT broker:

```bash
docker-compose up
```

#### 2. Environment variables
Create a `.env` file with the following variables in the root of the project to connect API with your MongoDB container created in the previous step:

```bash
MONGO_URI=mongodb://root:example@localhost:27017/
MONGO_DB=arkitech
MONGO_COLLECTION=hvac_data
```

#### 3. Create a Python environment with UV
If you have UV installed already, we advise you to create a Python environment:

On your terminal execute:

```bash
uv venv
```

Then activate your environment:

```bash
source .venv/bin/activate
```

#### 4. Run the backend API
In the same folder, you can run the Python backend with UV by executing the following commands. This will run a FastAPI server in your local machine:

```bash
uv sync
uv run fastapi dev
```

After running the command, you can go to `http://localhost:8000/docs` to see the API documentation (Swagger UI)
   
--- 

## Frontend setup
Path: `web-app/arkitech-dashboard`

Requirements:
- NodeJS version 20 or higher (you can use NVM to manage multiple versions of NodeJS)
  
### Instructions

#### Install NPM packages and run the Angular project
Go to the frontend folder `web-app/arkitech-dashboard` in the terminal and run the following commands to run the Angular project:

Install the NPM packages and run the Angular project:
```bash
npm install
ng dev
```

Open your browser and go to `http://localhost:4200/`

----

## Questions

- The day of the test we will share the tasks with you.
- If you have any questions, please feel free to reach out to us. We are happy to help you with any questions you may have setting up the project.

---