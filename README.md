
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


