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
    B <-- "8. Log daily activities" --> P8
    B <-- "9. Check vehicle health" --> P9
    B <-- "10. View performance" --> P7
    B <-- "11. View payments" --> P10
    P8 --> DB9
    P9 --> DB10
    P7 --> DB8
    P10 --> DB7
    
    %% Administrators
    C <-- "12. Manage fleet" --> P3
    C <-- "13. Create routes" --> P4
    C <-- "14. Assign vehicles" --> P5
    C <-- "15. Track performance" --> P7
    C <-- "16. Generate reports" --> P6
    C <-- "17. Manage payments" --> P10
    C <-- "18. Manage SACCO members" --> P11
    P3 --> DB3
    P4 --> DB4
    P5 --> DB6
    P6 --> DB1 & DB2 & DB3 & DB4 & DB5 & DB6 & DB7 & DB8 & DB9 & DB10
    P11 --> DB5
    
    %% SACCO Members
    D <-- "19. View shareholding