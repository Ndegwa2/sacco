# Sacco Management System

A comprehensive web-based management system for Savings and Credit Cooperative Organizations (SACCOs) specializing in transportation services.

## Overview

The Sacco Management System is designed to streamline the operations of transportation SACCOs by providing tools for fleet management, route planning, staff management, booking services, performance tracking, and financial reporting. The system caters to different user roles including administrators, employees (drivers/conductors), and passengers.

## Features

### User Management
- Multi-role user system (Admin, Employee, Passenger)
- Secure authentication with password hashing
- User registration and profile management
- Sacco membership tracking with shareholding information

### Fleet Management
- Vehicle registration and tracking
- Vehicle status monitoring
- Route assignment for vehicles
- Comprehensive fleet overview for administrators

### Route Management
- Create and manage transportation routes
- Define origins, destinations, and stops
- Track route status and performance
- Assign routes to employees

### Booking System
- Passenger trip booking
- Route selection
- Pickup and dropoff location specification
- Booking status tracking

### Performance Tracking
- Employee performance metrics
- Trip counting and monitoring
- Fare collection tracking
- Commission calculation
- Weekly and monthly performance reports

### Financial Management
- Employee payment processing
- Commission calculation
- Fare collection records
- Financial reporting and export capabilities

### Reporting
- CSV export functionality for various data
- Performance reports
- Payment summaries
- Route assignment reports

## Technology Stack

- **Backend**: Python Flask
- **Database**: MySQL (Production), SQLite (Testing)
- **ORM**: SQLAlchemy
- **Authentication**: Flask-Login
- **Frontend**: HTML, CSS, JavaScript
- **Migration**: Flask-Migrate

## Project Structure

```
Sacco_Management/
├── Client/                  # Static frontend files
├── instance/                # Instance-specific files
├── migrations/              # Database migration files
├── server/                  # Server-side code
│   ├── models/              # Database models
│   └── tests/               # Test files
├── static/                  # Static assets
│   └── styles/              # CSS files
├── templates/               # HTML templates
│   ├── admin/               # Admin interface templates
│   └── employee/            # Employee interface templates
├── config.py                # Application configuration
└── run.py                   # Application entry point
```

## Models

### User Models
- **User**: Core user model with authentication
- **SaccoMember**: Tracks SACCO membership and shareholding

### Vehicle Models
- **Vehicle**: Basic vehicle information
- **Fleet**: Extended vehicle management with status tracking

### Route Models
- **Route**: Transportation route definitions
- **AssignedRoute**: Links employees to routes

### Financial Models
- **EmployeePayment**: Tracks payments to employees
- **Performance**: Records employee performance metrics

### Booking Models
- **Booking**: Passenger booking information

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/Sacco_Management.git
   cd Sacco_Management
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. Run the application:
   ```
   python run.py
   ```

## Usage

### Admin Interface
- Access the admin dashboard at `/admin`
- Manage staff, fleet, routes, and view reports
- Track performance and financial data

### Employee Interface
- Access the employee dashboard at `/dashboard_employee.html`
- View assigned routes
- Check payment summaries
- Monitor performance metrics

### Passenger Interface
- Book trips through the booking interface
- View booking status and history

## Testing

Run tests using pytest:
```
pytest server/tests/
```

## Development Roadmap

- Implement more comprehensive reporting features
- Add mobile responsiveness to all interfaces
- Enhance security features
- Implement date validation in the booking system
- Standardize template naming and organization
- Improve user feedback after form submissions

## License



## Contributors

Samuel Ndegwa.

## Contact

For questions or support, please contact:
ndegwas03@gmail.com
