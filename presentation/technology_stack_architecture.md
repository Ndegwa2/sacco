# Slide 6: Technology Stack

## Backend Technologies
- **Python Flask**: Web framework for building the application
- **SQLAlchemy**: Object Relational Mapper (ORM) for database interactions
- **Flask-Login**: Authentication and session management
- **Flask-Migrate**: Database migration management

## Frontend Technologies
- **HTML5**: Markup language for structuring web pages
- **CSS3**: Styling and layout of web pages
- **JavaScript**: Client-side scripting for interactive features
- **Font Awesome**: Icon library for UI elements

## Database Technology
- **SQLite**: Development and testing database
- **MySQL**: Production database (planned for deployment)

## Deployment Platform
- **Render**: Cloud platform for deployment and hosting
- **Procfile**: Configuration for deployment on Render

## Development Tools
- **Visual Studio Code**: Primary IDE for development
- **Git**: Version control system
- **GitHub**: Code repository and collaboration platform

---

# Slide 7: System Architecture

## High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Passenger     │    │   Employee      │    │   Admin         │
│   Interface     │    │   Interface     │    │   Interface     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────────────┐
                    │      Flask Server       │
                    │  (Python Web Framework) │
                    └─────────────────────────┘
                                 │
                    ┌─────────────────────────┐
                    │    Database Layer       │
                    │   (SQLite/MySQL)        │
                    └─────────────────────────┘
```

## Component Interactions

1. **User Authentication Flow**
   - Users access the system through web interfaces
   - Flask server handles authentication requests
   - User credentials are verified against the database
   - Authenticated sessions are managed by Flask-Login

2. **Data Management Flow**
   - CRUD operations are handled by Flask routes
   - SQLAlchemy ORM translates requests to database queries
   - Database stores and retrieves all system data
   - Results are formatted and sent back to the client

3. **Business Logic Processing**
   - Performance calculations are done server-side
   - Booking validations are processed before confirmation
   - Payment calculations follow predefined business rules
   - Report generation aggregates data from multiple sources

## Security Considerations

- Password hashing for secure credential storage
- Role-based access control for different user types
- Input validation to prevent injection attacks
- Secure session management