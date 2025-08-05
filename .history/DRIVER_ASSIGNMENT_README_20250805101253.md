# Driver Route Assignment Scripts

This document explains the driver route assignment scripts created to fix the driver log dropdown issue.

## Problem Solved

The driver log dropdown was empty because there were no active route assignments in the database. These scripts create the necessary data structure:

1. **Driver users** with the 'employee' role
2. **Vehicles** for transportation
3. **Routes** for the drivers to operate on
4. **Route assignments** linking drivers to specific routes with vehicles

## Scripts Created

### 1. `assign_drivers_routes.py`

**Purpose**: Main script that creates drivers, vehicles, routes, and assigns them together.

**What it does**:
- Creates 3 driver users (if they don't exist):
  - John Kamau (driver001)
  - Mary Wanjiku (driver002) 
  - Peter Otieno (driver003)
- Creates 3 vehicles:
  - KCA 001A (Toyota Hiace)
  - KCB 002B (Nissan Matatu)
  - KCC 003C (Isuzu Forward)
- Creates 3 routes:
  - Nairobi-Thika Route
  - Nairobi-Kiambu Route
  - Nairobi-Machakos Route
- Assigns each driver to a route with a vehicle using the `AssignedRoute` model

**Usage**:
```bash
python assign_drivers_routes.py
```

**Expected Output**:
```
🚀 Starting Driver-Route Assignment Script
==================================================
✅ Database tables created/verified

📝 Step 1: Creating driver users...
✅ Created driver: John Kamau (driver001)
✅ Created driver: Mary Wanjiku (driver002)
✅ Created driver: Peter Otieno (driver003)

🚐 Step 2: Creating vehicles...
✅ Created vehicle: KCA 001A (Toyota Hiace)
✅ Created vehicle: KCB 002B (Nissan Matatu)
✅ Created vehicle: KCC 003C (Isuzu Forward)

🛣️  Step 3: Creating routes...
✅ Created route: Nairobi-Thika Route
✅ Created route: Nairobi-Kiambu Route
✅ Created route: Nairobi-Machakos Route

🔗 Step 4: Assigning drivers to routes...
✅ Assigned John Kamau to Nairobi-Thika Route with vehicle KCA 001A
✅ Assigned Mary Wanjiku to Nairobi-Kiambu Route with vehicle KCB 002B
✅ Assigned Peter Otieno to Nairobi-Machakos Route with vehicle KCC 003C

🔍 Step 5: Verifying assignments...
============================================================
VERIFICATION: Current Active Route Assignments
============================================================
👤 John Kamau -> 🛣️  Nairobi-Thika Route -> 🚐 KCA 001A
👤 Mary Wanjiku -> 🛣️  Nairobi-Kiambu Route -> 🚐 KCB 002B
👤 Peter Otieno -> 🛣️  Nairobi-Machakos Route -> 🚐 KCC 003C

Total active assignments: 3

🎉 SUCCESS: All drivers have been assigned to routes with vehicles!
💡 The driver log dropdown should now work properly.
```

### 2. `verify_driver_assignments.py`

**Purpose**: Verification script to check that all data needed for the driver log dropdown is properly set up.

**What it does**:
- Lists all drivers with 'employee' role
- Lists all active vehicles
- Lists all active routes
- Shows active route assignments
- Tests what data would appear in the driver log dropdown for each driver

**Usage**:
```bash
python verify_driver_assignments.py
```

## Database Models Used

### User Model
- Stores driver information with role='employee'
- Fields: username, email, full_name, role, status

### Vehicle Model
- Stores vehicle information
- Fields: plate_number, vehicle_model, status

### Route Model
- Stores route information
- Fields: route_name, origin, destination, stops, status

### AssignedRoute Model
- Links drivers to routes with vehicles
- Fields: employee_id, route_id, vehicle_id, start_date, end_date, status, shift, notes

## Driver Log Dropdown Fix

The driver log dropdown in `/employee/driver-log` now works because:

1. **Drivers exist**: There are users with role='employee'
2. **Active assignments exist**: Each driver has an active route assignment
3. **Vehicles are linked**: Each assignment includes a vehicle
4. **Routes are available**: Each assignment links to an active route

The dropdown query in the driver log template:
```python
assigned_routes = AssignedRoute.query.filter_by(
    employee_id=current_user.id,
    status='active'
).all()
```

Now returns data because we have created active assignments for each driver.

## Login Credentials

The created drivers can log in with:
- **Username**: driver001, driver002, driver003
- **Password**: driver123 (for all drivers)

## Running the Scripts

1. **First time setup**:
   ```bash
   python assign_drivers_routes.py
   ```

2. **Verify everything is working**:
   ```bash
   python verify_driver_assignments.py
   ```

3. **Re-run if needed**: The scripts are idempotent - they won't create duplicates if run multiple times.

## Troubleshooting

If the driver log dropdown is still empty:

1. Run the verification script to check data
2. Ensure the driver is logged in with an 'employee' role account
3. Check that the AssignedRoute query in the driver log template is correct
4. Verify database connectivity

## Files Modified/Created

- ✅ `assign_drivers_routes.py` - Main assignment script
- ✅ `verify_driver_assignments.py` - Verification script
- ✅ `DRIVER_ASSIGNMENT_README.md` - This documentation

The scripts integrate with the existing Flask application and database models without requiring any changes to the existing codebase.