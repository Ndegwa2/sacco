# 4.5.4 Entity Relationship Diagram and Database Schema

An Entity Relationship Diagram (ERD) is a structural diagram that illustrates the relationships between entities in a database. It is a critical tool in database design, providing a visual representation of how data is organized and how different data elements relate to one another. For the NaiSmart SACCO Management System, the ERD serves as a blueprint for the database implementation, ensuring data integrity and efficient query performance.

## Database Design Approach

The NaiSmart SACCO Management System database follows a normalized design approach to minimize redundancy and ensure data consistency. The schema is designed to support all core functionalities including user management, fleet tracking, route assignment, booking processing, employee performance monitoring, and vehicle health management.

## Key Entities and Relationships

The system database consists of 11 core entities that work together to support the complete functionality of the SACCO management system:

### 1. USER Entity
The USER entity serves as the foundation for all system access, supporting three distinct roles: admin, employee, and passenger. Each user has a unique username and email, with password security implemented through hashing. The entity includes status tracking for account management and full name for identification purposes.

### 2. SACCO_MEMBER Entity
This entity maintains records of SACCO membership information, including personal details and shareholding data. Each member is uniquely identified by their national ID number and email address.

### 3. VEHICLE Entity
The VEHICLE entity tracks all fleet vehicles with detailed information including plate numbers, models, and assignment status. It includes timestamps for creation and updates to maintain an audit trail of vehicle information changes.

### 4. ROUTE Entity
The ROUTE entity defines transportation routes with origin, destination, and intermediate stops. This entity is central to the booking system and vehicle assignment processes.

### 5. ASSIGNED_ROUTE Entity
This junction entity manages the relationship between employees (drivers) and routes, including vehicle assignments when applicable. It supports scheduling with start and end dates, shift assignments, and status tracking.

### 6. VEHICLE_ROUTE_ASSIGNMENT Entity
A secondary assignment entity that allows direct vehicle-to-route assignments without requiring a driver, providing flexibility in fleet management.

### 7. BOOKING Entity
The BOOKING entity manages passenger trip reservations with detailed information about routes, pickup/dropoff points, and scheduling. It links to users for authenticated bookings and includes status tracking for reservation management.

### 8. EMPLOYEE_PAYMENT Entity
This entity tracks financial compensation for employees based on trips completed and fare collection, supporting the SACCO's payment processing system.

### 9. PERFORMANCE Entity
The PERFORMANCE entity records employee productivity metrics including trips completed, fare collection, and commission earned, enabling performance analysis and improvement initiatives.

### 10. DRIVER_LOG Entity
This entity maintains daily operational logs for drivers, including mileage, earnings, and trip completion data. It provides detailed operational insights and supports fleet efficiency analysis.

### 11. VEHICLE_HEALTH Entity
The VEHICLE_HEALTH entity tracks vehicle condition assessments performed by drivers, using a standardized 1-5 scale for various vehicle systems. This supports proactive maintenance scheduling and vehicle safety management.

## Database Schema Implementation

The database schema has been implemented using SQLAlchemy ORM with PostgreSQL as the backend database. Key implementation features include:

### Data Integrity Constraints
- Primary keys ensure unique record identification across all entities
- Unique constraints prevent duplicate entries for critical fields such as usernames, emails, and plate numbers
- Foreign key relationships maintain referential integrity between related entities
- Not null constraints ensure required data is always present

### Data Types and Validation
- Proper data types are used for all fields (Integer, String, Date, Time, Float, Boolean)
- Date and time fields use appropriate types rather than strings for better querying and validation
- Enumerated values are used for status fields to ensure data consistency

### Audit Trail Features
- Created_at and updated_at timestamps track record modifications
- User references in assignment entities maintain accountability for administrative actions

## Relationship Cardinality

The database design implements various relationship cardinalities to support business requirements:

### One-to-Many Relationships
- One user can have multiple route assignments, payment records, performance entries, driver logs, and vehicle health checks
- One route can be assigned to multiple employees and vehicles
- One vehicle can participate in multiple route assignments, driver logs, and health checks

### Self-Referencing Relationships
- User entities reference themselves in assignment tracking (created_by fields)

## Design Benefits

The implemented database schema provides several advantages for the NaiSmart SACCO Management System:

1. **Scalability**: The normalized design supports growth in users, vehicles, and transactions
2. **Data Integrity**: Constraints and relationships ensure consistent, accurate data
3. **Performance**: Proper indexing strategies support efficient query execution
4. **Flexibility**: The dual assignment system (employee-route and vehicle-route) accommodates various operational models
5. **Auditability**: Comprehensive tracking supports accountability and analysis
6. **Security**: Role-based access is supported through the user entity structure

This database design forms the foundation for all system functionality, ensuring reliable data storage and retrieval while supporting the complex relationships required for effective SACCO management.

The figure below presents the Entity Relationship Diagram for the NaiSmart SACCO Management System.