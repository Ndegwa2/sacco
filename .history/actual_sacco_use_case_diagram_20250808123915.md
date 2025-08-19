# Sacco Management System - Actual Use Case Diagram

```mermaid
erDiagram
    %% Actors
    ADMIN ||--o{ MANAGE_USERS : "manages"
    ADMIN ||--o{ MANAGE_FLEET : "manages"
    ADMIN ||--o{ MANAGE_ROUTES : "manages"
    ADMIN ||--o{ ASSIGN_ROUTES : "assigns"
    ADMIN ||--o{ ASSIGN_VEHICLES : "assigns"
    ADMIN ||--o{ MANAGE_PERFORMANCE : "manages"
    ADMIN ||--o{ GENERATE_REPORTS : "generates"
    ADMIN ||--o{ MANAGE_SACCO_MEMBERS : "manages"
    
    EMPLOYEE ||--o{ UPDATE_VEHICLE_STATUS : "updates"
    EMPLOYEE