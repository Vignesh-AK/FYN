
# FYN

## Project Overview

**FYN** is a web application designed for managing vehicle workshops. It streamlines the process of handling customer bookings, vehicle maintenance, repair orders, and inventory management. The project features a Django-based backend for managing business logic and a React-based frontend for a responsive user interface.

## Getting Started

Follow the instructions below to set up and run the project on your local machine.

### Prerequisites

Ensure you have the following installed on your system:

- **Python 3.x**
- **pip** (Python package installer)
- **Node.js** and **npm**

### Backend Setup (Django)

1. **Navigate to the backend directory:**

   ```bash
   cd backend
   ```

2. **Create a virtual environment:**

   ```bash
   python3 -m venv env
   ```

3. **Activate the virtual environment:**

   ```bash
   source /env/bin/activate
   ```

4. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Apply migrations to set up the database:**

   ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```

6. **Run the Django development server:**

   ```bash
   python3 manage.py runserver
   ```

   The backend will now be running on `http://localhost:8000`.

### Frontend Setup (React)

1. **Navigate to the frontend directory:**

   ```bash
   cd frontend
   ```

2. **Install the necessary dependencies:**

   ```bash
   npm install
   ```

3. **Run the React development server:**

   ```bash
   npm start
   ```

   The app will be available in your browser at [http://localhost:3000](http://localhost:3000).

## Features

- **Backend (Django):** REST API to manage workshop operations like bookings, inventory, repair orders, and customer details.
- **Frontend (React):** User-friendly interface for workshop staff to manage daily tasks and track vehicles.
- **Booking Management:** List vehicles and their issues.
- **Inventory Management:** Keeps track of parts and other materials used in the workshop.

## Project Structure

```
FYN/
│
├── backend/
│   ├── DMS/ 
│      ├── env/                  # Python virtual environment
│      ├── manage.py             # Django management script
│      ├── requirements.txt      # Python dependencies
│      └── ...
│
└── frontend/
│   ├── vehicle-service-system/
│      ├── src/
│      ├── public/
│      └── package.json          # npm dependencies
```

## Available Scripts

### Backend

- **Run server:** `python3 manage.py runserver`
- **Apply migrations:** `python3 manage.py migrate`

### Frontend

- **Start development server:** `npm start`
