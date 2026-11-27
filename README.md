# Cloud-Based IoT Environmental Monitoring and Real-Time Alert System

## 1. Project Overview

This project implements a cloud-based environmental monitoring system designed to simulate environmental conditions inside a server room.

The system monitors temperature, humidity, workload, and cooling levels using simulated sensor data. It uses AWS cloud services to process and store environmental readings, detect abnormal temperature conditions, and generate automated email alerts.

A web-based dashboard provides separate interfaces for administrators and technicians to monitor environmental conditions and manage incidents.

## 2. Key Features

- **Environmental Monitoring:** Collects simulated temperature, humidity, workload, and cooling-level readings.
- **Automatic Cooling Control:** Adjusts cooling output based on the simulated temperature.
- **Threshold-Based Alerts:** Detects warning and critical temperature conditions.
- **Email Notifications:** Sends alerts through Amazon SNS when abnormal temperature conditions are detected.
- **Cloud Data Storage:** Stores environmental readings and incident records in Amazon DynamoDB.
- **Incident Management:** Allows technicians to acknowledge incidents, submit maintenance reports, and resolve incidents.
- **Role-Based Access:** Uses Amazon Cognito to authenticate users and distinguish between administrators and technicians.
- **Web Dashboard:** Provides environmental readings, active incidents, and incident history.

## 3. Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Web Framework | Flask |
| Cloud Platform | Amazon Web Services (AWS) |
| Authentication | Amazon Cognito |
| API Management | Amazon API Gateway |
| Serverless Computing | AWS Lambda |
| Database | Amazon DynamoDB |
| Notifications | Amazon SNS |
| Hosting | Render |
| Version Control | Git and GitHub |

## 4. System Architecture

The system follows a cloud-based architecture:

1. A Python simulator generates environmental readings.
2. The readings are transmitted to AWS through Amazon API Gateway.
3. AWS Lambda processes the incoming data and evaluates temperature thresholds.
4. Environmental readings and incident records are stored in Amazon DynamoDB.
5. Amazon SNS sends email notifications when abnormal temperature conditions are detected.
6. The Flask web application retrieves cloud data and displays it through administrator and technician dashboards.
7. Amazon Cognito handles user authentication and role-based dashboard access.

## 5. Temperature Thresholds

| Status | Temperature |
|---|---|
| Normal | 24°C or below |
| Warning | Above 24°C and below 27°C |
| Critical | 27°C or above |

Humidity is monitored as an additional environmental parameter but does not currently trigger automated alerts.

## 6. Repository Structure

```text
cloud_environment_monitor/
│
├── config/
├── cooling/
│   └── controller.py
│
├── dashboard/
│   ├── static/
│   │   ├── script.js
│   │   └── style.css
│   ├── templates/
│   │   ├── admin.html
│   │   └── technician.html
│   ├── __init__.py
│   └── app.py
│
├── database/
├── notifications/
├── reports/
├── simulator/
│   └── environment.py
│
├── tests/
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 7. Running the Project Locally

### Prerequisites

- Python 3.10 or later
- Git
- An AWS account with the required services configured
- An Amazon Cognito user pool and application client

### Step 1: Clone the repository

```bash
git clone https://github.com/Naman-Bhatnagar/cloud-environment-monitor.git
cd cloud-environment-monitor
```

### Step 2: Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows:**
```bash
.venv\Scripts\activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure environment variables

Create a `.env` file in the project root and configure the required application settings.

```env
FLASK_SECRET_KEY=your_secret_key
COGNITO_DOMAIN=your_cognito_domain
COGNITO_CLIENT_ID=your_cognito_client_id
COGNITO_CLIENT_SECRET=your_cognito_client_secret
COGNITO_ISSUER=your_cognito_issuer
APP_BASE_URL=http://localhost:5000
```

Do not upload your `.env` file or expose your credentials publicly.

### Step 5: Start the web application

```bash
python main.py
```

The local dashboard should be accessible at:

```text
http://localhost:5000
```

### Step 6: Start the environmental simulator

Run the simulator separately:

```bash
python simulator/environment.py
```

The simulator generates and transmits environmental readings to the AWS backend at regular intervals.

## 8. AWS API Endpoints

The application communicates with AWS through the following API Gateway routes:

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/readings` | Submit environmental readings |
| GET | `/readings` | Retrieve environmental readings |
| GET | `/incidents` | Retrieve active incidents |
| POST | `/incidents/update` | Update incident status and reports |
| GET | `/incidents/history` | Retrieve incident history |

## 9. Cloud Deployment

The Flask web application is deployed using Render.

AWS services provide the backend infrastructure for data processing, storage, authentication, and notifications.

The deployed application can be accessed at:

**https://cloud-environment-monitor.onrender.com**

The environmental simulator runs separately and must be started to generate new readings.

## 10. Important Notes

- Environmental readings are generated using a Python-based simulator rather than physical IoT sensors.
- The cooling controller is simulated and does not control physical cooling equipment.
- The AWS API endpoints currently do not have an API Gateway authorizer configured.
- AWS resources must be configured in the appropriate account and region for the application to function.
