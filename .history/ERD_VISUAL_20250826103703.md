# Visual ERD Diagram - Sacco Management System

```mermaid
erDiagram
    USER {
        int id PK
        string username
        string email
        string password_hash
        string role
        string full_name
        string status
    }
    
    SACCOMEMBER {
        int id PK
        string full_name
        string id_number
        string email
        string phone
        float shareholding
    }
    
    BOOKING {
        int id PK
        int user_id FK
        string route
        string pickup
        string dropoff
        date date
        time time
        string name
        string contact
        string status
        datetime created_at
    }
    
    ROUTE {
        int id PK
        string route_name
        string origin
        string destination
        string stops
        string status
    }
    
    VEHICLE {
        int id PK
        string plate_number
        string vehicle_model
        string assigned_route
        string status
        datetime created_at
        datetime updated_at
    }
    
    FLEET {
        int id PK
        string plate_number
        string vehicle_model
        string assigned_route
        string status
    }
    
    PERFORMANCE {
        int id PK
        int employee_id FK
        date date
        int trips
        float fare_collected
        float commission
        string route
    }
    
    DRIVERLOG {
        int id PK
        int driver_id FK
        int vehicle_id FK
        int route_id FK
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
    
    EMPLOYEEPAYMENT {
        int id PK
        int employee_id FK
        int total_trips
        float total_fare_collected
        float commission_earned
        string payment_status
        date payment_date
    }
    
    ASSIGNEDROUTE {
        int id PK
        int employee_id FK
        int route_id FK
        int vehicle_id FK
        datetime date_assigned
        date start_date
        date end_date
        string status
        string shift
        text notes
        int created_by FK
        datetime created_at
        datetime updated_at
    }
    
    VEHICLEROUTEASSIGNMENT {
        int id PK
        int vehicle_id FK
        int route_id FK
        datetime assigned_date
        date start_date
        date end_date
        string status
        string priority
        text notes
        int assigned_by FK
        datetime created_at
        datetime updated_at
    }
    
    VEHICLEHEALTH {
        int id PK
        int vehicle_id FK
        int driver_id FK
        datetime check_date
        int engine_condition
        int brake_condition
        int tire_condition
        int lights_condition
        int body_condition
        int fuel_level
        int oil_level
        int coolant_level
        text issues_noted
        boolean maintenance_needed
    }
    
    %% Relationships
    USER ||--o{ BOOKING : "makes"
    USER ||--o{ PERFORMANCE : "has"
    USER ||--o{ DRIVERLOG : "creates"
    USER ||--o{ EMPLOYEEPAYMENT : "receives"
    USER ||--o{ ASSIGNEDROUTE : "assigned_to"
    USER ||--o{ ASSIGNEDROUTE : "creates"
    USER ||--o{ VEHICLEROUTEASSIGNMENT : "creates"
    USER ||--o{ VEHICLEHEALTH : "checks"
    
    BOOKING }|--|| USER : "made_by"
    
    ROUTE ||--o{ ASSIGNEDROUTE : "assigned"
    ROUTE ||--o{ VEHICLEROUTEASSIGNMENT : "assigned"
    ROUTE ||--o{ DRIVERLOG : "logged"
    
    VEHICLE ||--o{ ASSIGNEDROUTE : "assigned"
    VEHICLE ||--o{ VEHICLEROUTEASSIGNMENT : "assigned"
    VEHICLE ||--o{ DRIVERLOG : "used"
    VEHICLE ||--o{ VEHICLEHEALTH : "checked"
    
    PERFORMANCE }|--|| USER : "belongs_to"
    
    DRIVERLOG }|--|| USER : "created_by"
    DRIVERLOG }|--|| VEHICLE : "uses"
    DRIVERLOG }|--|| ROUTE : "on"
    
    EMPLOYEEPAYMENT }|--|| USER : "for"
    
    ASSIGNEDROUTE }|--|| USER : "assigned_to"
    ASSIGNEDROUTE }|--|| ROUTE : "for"
    ASSIGNEDROUTE }|--|| VEHICLE : "using"
    ASSIGNEDROUTE }|--|| USER : "created_by"
    
    VEHICLEROUTEASSIGNMENT }|--|| VEHICLE : "assigned_to"
    VEHICLEROUTEASSIGNMENT }|--|| ROUTE : "for"
    VEHICLEROUTEASSIGNMENT }|--|| USER : "created_by"
    
    VEHICLEHEALTH }|--|| VEHICLE : "for"
    VEHICLEHEALTH }|--|| USER : "checked_by"