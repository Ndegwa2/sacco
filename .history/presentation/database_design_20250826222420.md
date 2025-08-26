# Slide 8: Database Design and ERD

## Entity Relationship Diagram

The NaiSmart SACCO Management System database consists of 12 core entities that capture all aspects of SACCO operations:

```
+----------------+          +----------------+
|    User        |          | SaccoMember    |
|----------------|          |----------------|
| id (PK)        |          | id (PK)        |
| username       |          | full_name      |
| email          |          | id_number      |
| password_hash  |          | email          |
| role           |          | phone          |
| full_name      |          | shareholding   |
| status         |          |                |
+----------------+          +----------------+
       | 1                           |
       |                           |
       | N                         |
+----------------+          +----------------+
|   Booking      |          |                |
|----------------|          |                |
| id (PK)        |          |                |
| user_id (FK)   |----------+                |
| route          |                           |
| pickup         |                           |
| dropoff        |                           |
| date           |                           |
| time           |                           |
| name           |                           |
| contact        |                           |
| status         |                           |
| created_at     |                           |
+----------------+                           |
                                             |
+----------------+          +----------------+
|   Performance  |          |   Route        |
|----------------|          |----------------|
| id (PK)        |          | id (PK)        |
| employee_id(FK)|----------| route_name     |
| date           |          | origin         |
| trips          |          | destination    |
| fare_collected |          | stops          |
| commission     |          | status         |
| route          |          |                |
+----------------+          +----------------+
       |                           | 1
       | N                         | |
+----------------+          +----------------+
| DriverLog      |          | AssignedRoute  |
|----------------|          |----------------|
| id (PK)        |          | id (PK)        |
| driver_id (FK) |----------| employee_id(FK)|
| vehicle_id (FK)|----------| route_id (FK)  |
| route_id (FK)  |----------| vehicle_id (FK)|
| log_date       |          | date_assigned  |
| starting_mileage|         | start_date     |
| ending_mileage |          | end_date       |
| total_distance |          | status         |
| total_earnings |          | shift          |
| fuel_cost      |          | notes          |
| maintenance_cost|         | created_by(FK) |
| net_earnings   |          | created_at     |
| trips_completed|          | updated_at     |
| passengers_served|         |                |
| notes          |          +----------------+
| created_at     |                   | 1
| updated_at     |                   | |
+----------------+                   | |
                                     | |
+----------------+          +----------------------+
|EmployeePayment |          |VehicleRouteAssignment|
|----------------|          |----------------------|
| id (PK)        |          | id (PK)              |
| employee_id(FK)|----------| vehicle_id (FK)      |
| total_trips    |          | route_id (FK)        |
| total_fare_collected|     | assigned_date        |
| commission_earned|        | start_date           |
| payment_status |          | end_date             |
| payment_date   |          | status               |
+----------------+          | priority             |
                            | notes                |
+----------------+          | assigned_by (FK)     |
| Vehicle        |          | created_at           |
|----------------|          | updated_at           |
| id (PK)        |          +----------------------+
| plate_number   |                   | 1
| vehicle_model  |                   | |
| assigned_route |                   | |
| status         |          +----------------+
| created_at     |          | VehicleHealth  |
| updated_at     |          |----------------|
+----------------+          | id (PK)        |
       | 1                  | vehicle_id (FK)|
       |                    | driver_id (FK) |
       | N                  | check_date     |
+----------------+          | engine_condition|
| Fleet          |          | brake_condition |
|----------------|          | tire_condition  |
| id (PK)        |          | lights_condition|
| plate_number   |          | body_condition  |
| vehicle_model  |          | fuel_level      |
| assigned_route |          | oil_level       |
| status         |          | coolant_level   |
+----------------+          | issues_noted    |
                            | maintenance_needed|
                            +------------------+
```

## Key Entities and Their Attributes

### 1. User
- **id** (Primary Key)
- **username**
- **email**
- **password_hash**
- **role** (admin, passenger, driver, employee)
- **full_name**
- **status** (active, inactive)

### 2. SaccoMember
- **id** (Primary Key)
- **full_name**
- **id_number** (Unique)
- **email**
- **phone**
- **shareholding**

### 3. Booking
- **id** (Primary Key)
- **user_id** (Foreign Key to User)
- **route**
- **pickup**
- **dropoff**
- **date**
- **time**
- **name**
- **contact**
- **status** (pending, confirmed, cancelled)
- **created_at**

### 4. Route
- **id** (Primary Key)
- **route_name**
- **origin**
- **destination**
- **stops**
- **status**

### 5. Vehicle
- **id** (Primary Key)
- **plate_number** (Unique)
- **vehicle_model**
- **assigned_route**
- **status** (active, inactive, maintenance)
- **created_at**
- **updated_at**

### 6. Performance
- **id** (Primary Key)
- **employee_id** (Foreign Key to User)
- **date**
- **trips**
- **fare_collected**
- **commission**
- **route**

### 7. DriverLog
- **id** (Primary Key)
- **driver_id** (Foreign Key to User)
- **vehicle_id** (Foreign Key to Vehicle)
- **route_id** (Foreign Key to Route)
- **log_date**
- **starting_mileage**
- **ending_mileage**
- **total_distance**
- **total_earnings**
- **fuel_cost**
- **maintenance_cost**
- **net_earnings**
- **trips_completed**
- **passengers_served**
- **notes**
- **created_at**
- **updated_at**

### 8. EmployeePayment
- **id** (Primary Key)
- **employee_id** (Foreign Key to User)
- **total_trips**
- **total_fare_collected**
- **commission_earned**
- **payment_status**
- **payment_date**

## Database Relationships

The database design implements several key relationships:

1. **User-Booking**: One-to-Many (One user can make many bookings)
2. **User-Performance**: One-to-Many (One user can have many performance records)
3. **User-DriverLog**: One-to-Many (One user can create many driver logs)
4. **User-EmployeePayment**: One-to-Many (One user can have many payment records)
5. **Route-AssignedRoute**: One-to-Many (One route can be assigned many times)
6. **Vehicle-DriverLog**: One-to-Many (One vehicle can be used in many driver logs)
7. **Vehicle-VehicleHealth**: One-to-Many (One vehicle can have many health checks)

These relationships ensure data integrity and enable complex queries for reporting and analytics.