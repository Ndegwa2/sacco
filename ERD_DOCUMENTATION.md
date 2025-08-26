# Entity Relationship Diagram (ERD) - Sacco Management System

## Entities and Their Attributes

### 1. User
- id (Primary Key)
- username
- email
- password_hash
- role (admin, passenger, driver, employee)
- full_name
- status (active, inactive)

### 2. SaccoMember
- id (Primary Key)
- full_name
- id_number (Unique)
- email
- phone
- shareholding

### 3. Booking
- id (Primary Key)
- user_id (Foreign Key to User)
- route
- pickup
- dropoff
- date
- time
- name
- contact
- status (pending, confirmed, cancelled)
- created_at

### 4. Route
- id (Primary Key)
- route_name
- origin
- destination
- stops
- status

### 5. Vehicle
- id (Primary Key)
- plate_number (Unique)
- vehicle_model
- assigned_route
- status (active, inactive, maintenance)
- created_at
- updated_at

### 6. Fleet
- id (Primary Key)
- plate_number (Unique)
- vehicle_model
- assigned_route
- status (active, inactive)

### 7. Performance
- id (Primary Key)
- employee_id (Foreign Key to User)
- date
- trips
- fare_collected
- commission
- route

### 8. DriverLog
- id (Primary Key)
- driver_id (Foreign Key to User)
- vehicle_id (Foreign Key to Vehicle)
- route_id (Foreign Key to Route)
- log_date
- starting_mileage
- ending_mileage
- total_distance
- total_earnings
- fuel_cost
- maintenance_cost
- net_earnings
- trips_completed
- passengers_served
- notes
- created_at
- updated_at

### 9. EmployeePayment
- id (Primary Key)
- employee_id (Foreign Key to User)
- total_trips
- total_fare_collected
- commission_earned
- payment_status
- payment_date

### 10. AssignedRoute (Route Assignment to Employee)
- id (Primary Key)
- employee_id (Foreign Key to User)
- route_id (Foreign Key to Route)
- vehicle_id (Foreign Key to Vehicle, nullable)
- date_assigned
- start_date
- end_date
- status (active, completed, cancelled)
- shift (morning, afternoon, evening)
- notes
- created_by (Foreign Key to User)
- created_at
- updated_at

### 11. VehicleRouteAssignment (Direct Vehicle to Route Assignment)
- id (Primary Key)
- vehicle_id (Foreign Key to Vehicle)
- route_id (Foreign Key to Route)
- assigned_date
- start_date
- end_date
- status (active, completed, cancelled)
- priority (high, normal, low)
- notes
- assigned_by (Foreign Key to User)
- created_at
- updated_at

### 12. VehicleHealth
- id (Primary Key)
- vehicle_id (Foreign Key to Vehicle)
- driver_id (Foreign Key to User)
- check_date
- engine_condition (1-5 scale)
- brake_condition (1-5 scale)
- tire_condition (1-5 scale)
- lights_condition (1-5 scale)
- body_condition (1-5 scale)
- fuel_level (1-5 scale)
- oil_level (1-5 scale)
- coolant_level (1-5 scale)
- issues_noted
- maintenance_needed
- created_at
- updated_at

## Relationships

### User Relationships
- One User can have many Bookings (1:N)
- One User can have many Performances (1:N)
- One User can have many DriverLogs (1:N)
- One User can have many EmployeePayments (1:N)
- One User can have many AssignedRoutes (1:N)
- One User can create many AssignedRoutes (1:N)
- One User can create many VehicleRouteAssignments (1:N)
- One User can perform many VehicleHealth checks (1:N)

### SaccoMember Relationships
- No direct relationships with other entities

### Booking Relationships
- One Booking belongs to one User (N:1)

### Route Relationships
- One Route can be assigned to many AssignedRoutes (1:N)
- One Route can have many VehicleRouteAssignments (1:N)
- One Route can have many DriverLogs (1:N)

### Vehicle Relationships
- One Vehicle can be assigned to many AssignedRoutes (1:N)
- One Vehicle can have many VehicleRouteAssignments (1:N)
- One Vehicle can have many DriverLogs (1:N)
- One Vehicle can have many VehicleHealth checks (1:N)

### Performance Relationships
- One Performance belongs to one User (N:1)

### DriverLog Relationships
- One DriverLog belongs to one User (N:1)
- One DriverLog belongs to one Vehicle (N:1)
- One DriverLog belongs to one Route (N:1)

### EmployeePayment Relationships
- One EmployeePayment belongs to one User (N:1)

### AssignedRoute Relationships
- One AssignedRoute belongs to one User (N:1)
- One AssignedRoute belongs to one Route (N:1)
- One AssignedRoute belongs to one Vehicle (N:1)
- One AssignedRoute is created by one User (N:1)

### VehicleRouteAssignment Relationships
- One VehicleRouteAssignment belongs to one Vehicle (N:1)
- One VehicleRouteAssignment belongs to one Route (N:1)
- One VehicleRouteAssignment is created by one User (N:1)

### VehicleHealth Relationships
- One VehicleHealth check belongs to one Vehicle (N:1)
- One VehicleHealth check belongs to one User (N:1)

## ERD Diagram (Text Representation)

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
| vehicle_id(FK) |----------| route_id (FK)  |
| route_id (FK)  |----------| vehicle_id(FK) |
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
       | 1                  | vehicle_id(FK) |
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

## Notes

1. PK = Primary Key
2. FK = Foreign Key
3. The Fleet entity appears to be a duplicate of Vehicle and might be consolidated
4. User roles determine access levels and functionality in the system
5. All timestamp fields (created_at, updated_at, check_date, etc.) are automatically managed by the system
6. Status fields are used to track the current state of entities in the system
7. The system supports both direct vehicle-to-route assignments and driver-assigned route assignments