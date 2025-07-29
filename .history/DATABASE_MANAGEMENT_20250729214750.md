# PostgreSQL Database Management Guide

Your Sacco Management system is now connected to a PostgreSQL database hosted on Render. Here are several ways to view and manage your database with a GUI interface similar to phpMyAdmin.

## Database Connection Details

- **Host:** `dpg-d24gta3uibrs73bur5r0-a.oregon-postgres.render.com`
- **Port:** `5432`
- **Database:** `sacco_postgre`
- **Username:** `sacco_postgre_user`
- **Password:** `b91ItAmZMAFi1a1jrVpCPEAviOTH1JLO`

## Option 1: Custom Database Viewer (Recommended for Quick Access)

I've created a simple web-based database viewer for you:

```bash
# Run the database viewer
python database_viewer.py
```

Then open your browser and go to: **http://localhost:5001**

Features:
- ✅ View all tables in your database
- ✅ Browse table data (up to 100 rows per table)
- ✅ Clean, responsive web interface
- ✅ No additional software installation required

## Option 2: pgAdmin (Most Popular PostgreSQL GUI)

### Installation:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install pgadmin4

# Or install via pip
pip install pgadmin4
```

### Setup:
1. Open pgAdmin
2. Right-click "Servers" → "Create" → "Server"
3. **General Tab:**
   - Name: `Sacco Database`
4. **Connection Tab:**
   - Host: `dpg-d24gta3uibrs73bur5r0-a.oregon-postgres.render.com`
   - Port: `5432`
   - Database: `sacco_postgre`
   - Username: `sacco_postgre_user`
   - Password: `b91ItAmZMAFi1a1jrVpCPEAviOTH1JLO`
5. Click "Save"

## Option 3: DBeaver (Cross-platform, Free)

### Installation:
1. Download from: https://dbeaver.io/download/
2. Or install via snap: `sudo snap install dbeaver-ce`

### Setup:
1. Open DBeaver
2. Click "New Database Connection"
3. Select "PostgreSQL"
4. Enter connection details:
   - **Server Host:** `dpg-d24gta3uibrs73bur5r0-a.oregon-postgres.render.com`
   - **Port:** `5432`
   - **Database:** `sacco_postgre`
   - **Username:** `sacco_postgre_user`
   - **Password:** `b91ItAmZMAFi1a1jrVpCPEAviOTH1JLO`
5. Test connection and save

## Option 4: Adminer (Web-based, like phpMyAdmin)

### Setup:
1. Download Adminer: https://www.adminer.org/
2. Place `adminer.php` in your web server directory
3. Access via browser: `http://localhost/adminer.php`
4. Login with:
   - **System:** PostgreSQL
   - **Server:** `dpg-d24gta3uibrs73bur5r0-a.oregon-postgres.render.com:5432`
   - **Username:** `sacco_postgre_user`
   - **Password:** `b91ItAmZMAFi1a1jrVpCPEAviOTH1JLO`
   - **Database:** `sacco_postgre`

## Option 5: Command Line Access

You can also access your database directly via command line:

```bash
# Using the provided PSQL command
PGPASSWORD=b91ItAmZMAFi1a1jrVpCPEAviOTH1JLO psql -h dpg-d24gta3uibrs73bur5r0-a.oregon-postgres.render.com -U sacco_postgre_user sacco_postgre

# Common PostgreSQL commands:
\dt          # List all tables
\d tablename # Describe table structure
SELECT * FROM users LIMIT 10;  # View data
\q           # Quit
```

## Current Database Tables

Your Sacco Management system has the following tables:
- `user` - System users (admin, employee, passenger)
- `route` - Transportation routes
- `booking` - Passenger bookings
- `fleet` - Vehicle fleet management
- `performance` - Employee performance tracking
- `employee_payment` - Payment records
- `assigned_route` - Route assignments
- `driver_log` - Daily driver logs
- `vehicle_health` - Vehicle health checks
- `sacco_member` - Sacco membership records

## Security Notes

⚠️ **Important:** The database credentials are stored in your `.env` file. Keep this file secure and never commit it to version control.

🔒 **Production:** Consider using environment variables or secure credential management in production deployments.

## Troubleshooting

If you encounter connection issues:
1. Ensure your internet connection is stable
2. Check if the Render database service is running
3. Verify the connection details are correct
4. Try connecting via command line first to test connectivity