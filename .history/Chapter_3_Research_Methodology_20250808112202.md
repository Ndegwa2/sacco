# Chapter 3: Research Methodology

## 3.1 Introduction

This chapter presents the research methodology employed in the development of the NaiSmart SACCO Management System. It details the systematic approach used in designing, implementing, and validating the system to ensure it meets the functional and non-functional requirements of SACCO transportation management. The methodology encompasses the research approach, system architecture design, database modeling, implementation strategy, and validation techniques used throughout the development lifecycle.

## 3.2 Research Approach

The development of the NaiSmart system followed an iterative and incremental software development methodology, specifically adopting principles from the Agile methodology combined with elements of the Spiral model. This approach was chosen to accommodate the evolving requirements of SACCO transportation management and to ensure continuous feedback from stakeholders throughout the development process.

### 3.2.1 Problem Analysis

The research began with a comprehensive analysis of the challenges faced by SACCOs in managing their transportation services. Key issues identified included:
- Inefficient route assignment and vehicle allocation
- Lack of real-time performance tracking for drivers
- Manual booking systems leading to errors and inefficiencies
- Absence of systematic vehicle health monitoring
- Inadequate financial tracking and commission management

### 3.2.2 Requirements Gathering

Requirements were gathered through multiple approaches:
1. **Stakeholder Interviews**: Conducted with SACCO administrators, drivers, and passengers to understand their needs
2. **Observation**: Direct observation of existing manual processes in SACCO operations
3. **Document Analysis**: Review of existing transportation management procedures and policies
4. **Benchmarking**: Analysis of similar systems in the transportation industry

### 3.2.3 System Design Approach

The system design followed a user-centered design approach with emphasis on:
- Usability and accessibility for different user roles (admin, employee/driver, passenger)
- Scalability to accommodate growing SACCO operations
- Security to protect sensitive data
- Maintainability for future enhancements

## 3.3 System Architecture and Design Methodology

### 3.3.1 Architectural Pattern

The NaiSmart system was developed using the Model-View-Controller (MVC) architectural pattern, which separates the application into three interconnected components:

1. **Model**: Represents the data structure and business logic of the system
2. **View**: Handles the user interface and presentation layer
3. **Controller**: Manages user input and coordinates between Model and View

This pattern was chosen for its:
- Clear separation of concerns
- Enhanced maintainability
- Improved testability
- Better code organization

### 3.3.2 Technology Stack

The system was implemented using the following technologies:

#### Backend Technologies:
- **Python**: Primary programming language
- **Flask**: Web framework for building the application
- **SQLAlchemy**: Object-Relational Mapping (ORM) library for database interactions
- **SQLite/PostgreSQL**: Database management systems

#### Frontend Technologies:
- **HTML5**: Markup language for structuring web pages
- **CSS3**: Styling language for presentation
- **JavaScript**: Programming language for client-side interactivity
- **Jinja2**: Template engine for dynamic content rendering

#### Development Tools:
- **Git**: Version control system
- **VS Code**: Integrated Development Environment
- **Render**: Deployment platform

### 3.3.3 System Components

The NaiSmart system consists of the following core components:

1. **User Management Module**: Handles user authentication, authorization, and role-based access control
2. **Fleet Management Module**: Manages vehicle information, status, and assignments
3. **Route Management Module**: Defines transportation routes with origins, destinations, and stops
4. **Booking Management Module**: Facilitates passenger bookings and trip scheduling
5. **Assignment Management Module**: Handles driver-route and vehicle-route assignments
6. **Performance Tracking Module**: Monitors driver performance metrics
7. **Financial Management Module**: Tracks earnings, commissions, and payments
8. **Vehicle Health Monitoring Module**: Records vehicle condition assessments
9. **Reporting Module**: Generates analytical reports for administrators

## 3.4 Database Design Methodology

### 3.4.1 Database Design Approach

The database design followed a systematic approach involving:

1. **Requirements Analysis**: Identification of data entities and relationships from system requirements
2. **Conceptual Design**: Creation of Entity-Relationship (ER) diagrams to model data entities
3. **Logical Design**: Translation of ER diagrams into relational schemas
4. **Physical Design**: Optimization of database structure for performance

### 3.4.2 Database Schema Design

The database schema was designed to support all system functionalities with the following key entities:

#### User Management Tables:
- **user**: Stores user information with role-based access control (admin, employee, passenger)
- **sacco_member**: Tracks SACCO membership and shareholding information

#### Fleet Management Tables:
- **vehicle**: Contains vehicle information including plate numbers, models, and status

#### Route Management Tables:
- **route**: Defines transportation routes with origins, destinations, and stops

#### Assignment Tables:
- **assigned_route**: Links employees (drivers) to routes with vehicle assignments
- **vehicle_route_assignment**: Direct vehicle-to-route assignments without requiring a driver

#### Booking System Tables:
- **booking**: Records passenger trip bookings with scheduling information

#### Financial Management Tables:
- **employee_payment**: Tracks payments to employees based on performance
- **performance**: Records employee performance metrics including trips and earnings

#### Operations Tables:
- **driver_log**: Daily driver activity logging with mileage and earnings information
- **vehicle_health**: Vehicle condition monitoring and maintenance tracking

### 3.4.3 Normalization Process

The database schema was normalized to:
- Eliminate data redundancy
- Ensure data integrity
- Improve storage efficiency
- Enhance query performance

The schema achieves Third Normal Form (3NF) by ensuring:
- Each table has a primary key
- Non-key attributes are functionally dependent on the primary key
- No transitive dependencies exist

### 3.4.4 Relationship Mapping

The database design implements the following relationships:
- One-to-Many relationships between users and their assignments, payments, and performance records
- Many-to-Many relationships between routes and vehicles through assignment tables
- One-to-Many relationships between vehicles and their health checks and driver logs

## 3.5 Implementation Methodology

### 3.5.1 Development Approach

The implementation followed an iterative development approach with the following phases:

#### Phase 1: Core Infrastructure Development
- Setup of development environment
- Configuration of Flask application
- Implementation of database models
- User authentication system

#### Phase 2: Module Development
- Sequential development of system modules
- Implementation of CRUD operations for each entity
- Integration of business logic
- Development of user interfaces

#### Phase 3: Integration and Testing
- Integration of all modules
- System testing and debugging
- Performance optimization
- Security enhancements

### 3.5.2 Coding Standards

The implementation followed established coding standards:
- **PEP 8**: Python coding conventions
- **Modular Design**: Separation of concerns through well-defined modules
- **Documentation**: Inline comments and docstrings for code clarity
- **Error Handling**: Comprehensive exception handling mechanisms

### 3.5.3 Version Control

Git was used for version control with:
- Feature branching strategy
