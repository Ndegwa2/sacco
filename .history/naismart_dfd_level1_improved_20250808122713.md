# NaiSmart SACCO Management System - Improved DFD Level 1

## Data Flow Diagram (Level 1)

```mermaid
graph TD
    %% External Entities (Yellow)
    A[Passengers]:::external
    B[Drivers/Conductors]:::external
    C[Administrators]:::external
    D[SACCO Members]:::external
    E[Payment Systems]:::external
    F[Vehicle Maintenance Services]:::external
    
    %% Core Processes (Rounded Purple)
    P1[1.0 Register/Login]:::process
    P2[2.0 Book Trip]:::process
    P3[3.0 Manage Fleet]:::process
    P4[4.0 Create Routes]:::process
    P5[5.0 Assign Fleet]:::process
    P6[6.0 Generate Reports]:::process
    P7[7.0 Track Performance]:::process
    P8[8.0 Log Driver Activities]:::process
    P9[9.0 Monitor Vehicle Health]:::process
    P10[10.0 Manage Payments]:::process
    P11[11.0 Manage SACCO Members]:::process
    
    %% Data Stores (Blue)
    DB1[User DB]:::datastore
    DB2[Booking DB]:::datastore
    DB3[Vehicle DB]:::datastore
    DB4[Route DB]:::datastore
    DB5[SACCO Member DB]:::datastore
    DB6[Assignment DB]:::datastore
    DB7[Payment DB]:::datastore
    DB8[Performance DB]:::datastore
    DB9[Driver Log DB]:::datastore
    DB10[Vehicle Health DB]:::datastore
    
    %% Data Flows
    %% Passengers
    A <-- "1. Register/Login requests" --> P1
    A <-- "2. Trip booking requests" --> P2
    A <-- "3. View booking history" --> DB2
    P1 <-- "4. Authentication data" --> DB1
    P2 <-- "5. Booking records" --> DB2
    DB2 -- "6. Booking confirmations" --> A
    
    %% Drivers/Conductors
    B <-- "7. View assignments" --> P5
    B <--