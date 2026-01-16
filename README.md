# HealthSync ![Build Status](https://img.shields.io/badge/build-passing-brightgreen) ![Version](https://img.shields.io/badge/version-1.0.0-blue)

## Project Description
HealthSync is a web application that aggregates health data from various wearable devices and provides users with personalized insights and recommendations. It allows users to securely share their health information with healthcare providers, facilitating better health management and communication.

## Features
- 📊 Real-time health data integration from various wearable devices
- 🤖 Personalized health insights and recommendations using AI
- 🔒 Secure sharing of health data with healthcare providers

## Tech Stack
### Frontend
- **Next.js** 🌐

### Backend
- **FastAPI** 🚀
- **LangChain** 📚
- **OpenAI** 🤖

### Database
- **PostgreSQL** 🗄️

## Installation
To set up the project locally, follow these steps:

- Clone the repository
bash
git clone https://github.com/yuvraj-singh-codes/healthsync
- Navigate into the project directory
bash
cd healthsync
- Install the backend dependencies
bash
cd backend
pip install -r requirements.txt
- Install the frontend dependencies
bash
cd ../frontend
npm install
- Set up the PostgreSQL database
bash
# Ensure PostgreSQL is running and create a database
createdb healthsync
## Usage
To run the application locally, follow these steps:

- Start the backend server
bash
cd backend
uvicorn main:app --reload
- Start the frontend development server
bash
cd ../frontend
npm run dev
- Open your browser and navigate to `http://localhost:3000` to access the application.

## API Documentation
For detailed API documentation, please refer to the [API Docs](https://github.com/yuvraj-singh-codes/healthsync/wiki/API-Documentation).

## Testing
To run the tests for the backend, execute the following command:

bash
cd backend
pytest
## Deployment
For deploying the application, follow these steps:

- Build the frontend for production
bash
cd frontend
npm run build
- Deploy the backend using your preferred cloud service (e.g., AWS, Heroku).

## Contributing
We welcome contributions! Please follow these guidelines:

- Fork the repository
- Create a new branch for your feature or bug fix
- Commit your changes
- Push to your branch
- Open a pull request

Thank you for your interest in contributing to HealthSync!