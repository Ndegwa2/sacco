# Naismart SACCO Management System - Entity Relationship Diagram

## Enhanced ERD with Crow's Foot Notation

```mermaid
erDiagram
    USER {
        int id PK "Primary Key"
        string username UK "Unique"
        string email UK "Unique"
        string password_hash
        string role "admin/employee/passenger"
        string full_name
        string status "active/inactive"
    }
    
    SACCO_MEMBER {
        int id PK "Primary Key"
        string full_name
        string id_number UK "Unique"
        string email UK "Unique"
        string phone
        float shareholding
    }
    
    VEHICLE {
        int id PK "Primary Key"
        string plate_number UK "Unique"
        string vehicle_model
        string assigned_route
        string status "active/inactive/maintenance"
        datetime created_at
        datetime updated_at
    }
    
    FLEET {
        int id PK "Primary Key"
        string plate_number UK "Unique"
        string vehicle_model
        string assigned_route
        string status "active/inactive"
    }
    
    ROUTE {
        int id PK "Primary Key"
        string route_name
        string origin
        string destination
        string stops
        string status "active/inactive"
    }
    
    ASSIGNED_ROUTE {
        int id PK "Primary Key"
        int employee_id FK "References USER.id"
        int route_id FK "References ROUTE.id"
        int vehicle_id FK "References VEHICLE.id"
        datetime date_assigned
        date start_date
        date end_date
        string status "active/completed/cancelled"
        string shift "morning/afternoon/evening"
        text notes
        int created_by FK "References USER.id"
        datetime created_at
        datetime updated_at
    }
    
    VEHICLE_ROUTE_ASSIGNMENT {
        int id PK "Primary Key"
        int vehicle_id FK "References VEHICLE.id"
        int route_id FK "References ROUTE.id"
        datetime assigned_date
        date start_date
        date end_date
        string status "active/completed/cancelled"
        string priority "high/normal/low"
        text notes
        int assigned_by FK "References USER.id"
        datetime created_at
        datetime updated_at
    }
    
    BOOKING {
        int id PK "Primary Key"
        string route
        string pickup
        string dropoff
        string date "String format - needs conversion"
        string time "String format"
        string name
        string contact
        string status "pending/confirmed/cancelled"
    }
    
    EMPLOYEE_PAYMENT {
        int id PK "Primary Key"
        int employee_id FK "References USER.id"
        int total_trips
        float total_fare_collected
        float commission_earned
        string payment_status "pending/paid/cancelled"
        date payment_date
    }
    
    PERFORMANCE {
        int id PK "Primary Key"
        int employee_id FK "References USER.id"
        date date
        int trips
        float fare_collected
        float commission
        string route
    }
    
    DRIVER_LOG {
        int id PK "Primary Key"
        int driver_id FK "References USER.id"
        int vehicle_id FK "References VEHICLE.id"
        int route_id FK "References ROUTE.id"
        date log_date
        float starting_mileage
        float ending_mileage
        float total_distance
        float total_earnings
        float fuel_cost
        float maintenance_cost
        float net_earnings
        int trips_completed
        int passengers_served
        text notes
        datetime created_at
        datetime updated_at
    }
    
    VEHICLE_HEALTH {
        int id PK "Primary Key"
        int vehicle_id FK "References VEHICLE.id"
        int driver_id FK "References USER.id"
        datetime check_date
        int engine_condition "Scale 1-5"
        int brake_condition "Scale 1-5"
        int tire_condition "Scale 1-5"
        int lights_condition "Scale 1-5"
        int body_condition "Scale 1-5"
        int fuel_level "Scale 1-5"
        int oil_level "Scale 1-5"
        int coolant_level "Scale 1-5"
        text issues_noted
        boolean maintenance_needed
    }

    %% Relationships with Crow's Foot Notation
    
    %% USER relationships (One-to-Many)
    USER ||--o{ ASSIGNED_ROUTE : "employee_id (One User can have Many Route Assignments)"
    USER ||--o{ ASSIGNED_ROUTE : "created_by (One Admin creates Many Assignments)"
    USER ||--o{ VEHICLE_ROUTE_ASSIGNMENT : "assigned_by (One Admin creates Many Vehicle Assignments)"
    USER ||--o{ EMPLOYEE_PAYMENT : "employee_id (One Employee has Many Payments)"
    USER ||--o{ PERFORMANCE : "employee_id (One Employee has Many Performance Records)"
    USER ||--o{ DRIVER_LOG : "driver_id (One Driver has Many Log Entries)"
    USER ||--o{ VEHICLE_HEALTH : "driver_id (One Driver performs Many Health Checks)"
    
    %% ROUTE relationships (One-to-Many)
