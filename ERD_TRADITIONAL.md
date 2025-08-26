# Traditional ERD - Sacco Management System

## Entity Relationship Diagram

```plaintext
                    +------------------+
                    |    SaccoMember   |
                    +------------------+
                    | id (PK)          |
                    | full_name        |
                    | id_number        |
                    | email            |
                    | phone            |
                    | shareholding     |
                    +------------------+
                           |
                           | (0,N)
                           |
                    +------------------+
                    |      User        |
                    +------------------+
                    | id (PK)          |
                    | username         |
                    | email            |
                    | password_hash    |
                    | role             |
                    | full_name        |
                    | status           |
                    +------------------+
                     |       |        |
         (1,1)       |       |        | (0,N)
            +--------+       |        +------------------+
            |                |                           |
            |                | (0,N)                     |
  +------------------+  +--------+              +------------------+
  |    Booking       |  |        |              |   Performance    |
  +------------------+  |        |              +------------------+
  | id (PK)          |  |        |              | id (PK)          |
  | user_id (FK)     |--+        |              | employee_id (FK) |
  | route            |           |              | date             |
  | pickup           |           |              | trips            |
  | dropoff          |           |              | fare_collected   |
  | date             |           |              | commission       |
  | time             |           |              | route            |
  | name             |           |              +------------------+
  | contact          |           |
  | status           |           |
  | created_at       |           |
  +------------------+           |
                                 |
                        +------------------+
                        |   EmployeePayment|
                        +------------------+
                        | id (PK)          |
                        | employee_id (FK) |
                        | total_trips      |
                        | total_fare_collected |
                        | commission_earned |
                        | payment_status   |
                        | payment_date     |
                        +------------------+

                    +------------------+
                    |      Route       |
                    +------------------+
                    | id (PK)          |
                    | route_name       |
                    | origin           |
                    | destination      |
                    | stops            |
                    | status           |
                    +------------------+
                     |        |        |
         (0,N)       |        |        | (0,N)
            +--------+        |        +--------+
            |                 |                 |
  +------------------+  +------------------+  +------------------+
  | AssignedRoute    |  |VehicleRouteAssig.|  |   DriverLog      |
  +------------------+  +------------------+  +------------------+
  | id (PK)          |  | id (PK)          |  | id (PK)          |
  | employee_id (FK) |  | vehicle_id (FK)  |  | driver_id (FK)   |
  | route_id (FK)    |--| route_id (FK)    |--| route_id (FK)    |
  | vehicle_id (FK)  |  | assigned_date    |  | vehicle_id (FK)  |
  | date_assigned    |  | start_date       |  | log_date         |
  | start_date       |  | end_date         |  | starting_mileage |
  | end_date         |  | status           |  | ending_mileage   |
  | status           |  | priority         |  | total_distance   |
  | shift            |  | notes            |  | total_earnings   |
  | notes            |  | assigned_by (FK) |  | fuel_cost        |
  | created_by (FK)  |  | created_at       |  | maintenance_cost |
  | created_at       |  | updated_at       |  | net_earnings     |
  | updated_at       |  +------------------+  | trips_completed  |
  +------------------+                      | passengers_served|
                                            | notes            |
                                            | created_at       |
                                            | updated_at       |
                                            +------------------+

                    +------------------+
                    |     Vehicle      |
                    +------------------+
                    | id (PK)          |
                    | plate_number     |
                    | vehicle_model    |
                    | assigned_route   |
                    | status           |
                    | created_at       |
                    | updated_at       |
                    +------------------+
                     |        |        |
         (0,N)       |        |        | (0,N)
            +--------+        |        +--------+
            |                 |                 |
  +------------------+  +------------------+  +------------------+
  |     Fleet        |  |                  |  |  VehicleHealth   |
  +------------------+  |                  |  +------------------+
  | id (PK)          |  |                  |  | id (PK)          |
  | plate_number     |  |                  |  | vehicle_id (FK)  |
  | vehicle_model    |  |                  |  | driver_id (FK)   |
  | assigned_route   |  |                  |  | check_date       |
  | status           |  |                  |  | engine_condition |
  +------------------+  |                  |  | brake_condition  |
                        |                  |  | tire_condition   |
                        |                  |  | lights_condition |
                        |                  |  | body_condition   |
                        |                  |  | fuel_level       |
                        |                  |  | oil_level        |
                        |                  |  | coolant_level    |
                        |                  |  | issues_noted     |
                        |                  |  | maintenance_needed|
                        |                  |  +------------------+
                        |                  |
                        +------------------+
```

## Relationship Summary

1. **User - Booking**: One-to-Many (One user can make many bookings)
2. **User - Performance**: One-to-Many (One user can have many performance records)
3. **User - EmployeePayment**: One-to-Many (One user can have many payment records)
4. **User - AssignedRoute**: One-to-Many (One user can be assigned to many routes)
5. **User - DriverLog**: One-to-Many (One user can create many driver logs)
6. **User - VehicleHealth**: One-to-Many (One user can perform many vehicle health checks)
7. **User - AssignedRoute (created_by)**: One-to-Many (One user can create many route assignments)
8. **User - VehicleRouteAssignment (assigned_by)**: One-to-Many (One user can create many vehicle route assignments)

9. **Route - AssignedRoute**: One-to-Many (One route can be assigned many times)
10. **Route - VehicleRouteAssignment**: One-to-Many (One route can be assigned to many vehicles)
11. **Route - DriverLog**: One-to-Many (One route can have many driver logs)

12. **Vehicle - AssignedRoute**: One-to-Many (One vehicle can be assigned to many routes)
13. **Vehicle - VehicleRouteAssignment**: One-to-Many (One vehicle can be assigned to many routes)
14. **Vehicle - DriverLog**: One-to-Many (One vehicle can be used in many driver logs)
15. **Vehicle - VehicleHealth**: One-to-Many (One vehicle can have many health checks)
16. **Vehicle - Fleet**: One-to-One (One vehicle corresponds to one fleet record)

## Notes

- PK = Primary Key
- FK = Foreign Key
- (0,N) = Zero to Many relationship
- (1,1) = One to One relationship
- The Fleet entity appears to duplicate information from Vehicle and might be consolidated
- All relationships are bidirectional, allowing navigation from either entity