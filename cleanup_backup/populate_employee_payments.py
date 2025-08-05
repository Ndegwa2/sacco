#!/usr/bin/env python3
"""
Script to populate EmployeePayment records from existing Performance and DriverLog data
"""

import sys
import os
from datetime import datetime, date
from collections import defaultdict

# Add the current directory to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from run import app, db, EmployeePayment, Performance, DriverLog, User

def populate_employee_payments():
    """Create EmployeePayment records from Performance and DriverLog data"""
    
    with app.app_context():
        print("🔄 Starting EmployeePayment population...")
        
        # Get all employees
        employees = User.query.filter_by(role='employee').all()
        print(f"📊 Found {len(employees)} employees")
        
        # Get all performance and driver log records
        performances = Performance.query.all()
        driver_logs = DriverLog.query.all()
        
        print(f"📊 Found {len(performances)} performance records")
        print(f"📊 Found {len(driver_logs)} driver log records")
        
        # Group data by employee and date
        payment_data = defaultdict(lambda: {
            'total_trips': 0,
            'total_fare_collected': 0.0,
            'commission_earned': 0.0,
            'dates': set()
        })
        
        # Process Performance records
        for perf in performances:
            key = (perf.employee_id, perf.date)
            payment_data[key]['total_trips'] += perf.trips or 0
            payment_data[key]['total_fare_collected'] += perf.fare_collected or 0.0
            payment_data[key]['commission_earned'] += perf.commission or 0.0
            payment_data[key]['dates'].add(perf.date)
        
        # Process DriverLog records
        for log in driver_logs:
            key = (log.driver_id, log.log_date)
            payment_data[key]['total_trips'] += log.trips_completed or 0
            payment_data[key]['total_fare_collected'] += log.total_earnings or 0.0
            # Calculate commission as 10% of earnings if not already set
            if key not in [k for k in payment_data.keys() if k[0] == log.driver_id]:
                payment_data[key]['commission_earned'] += (log.total_earnings or 0.0) * 0.1
            payment_data[key]['dates'].add(log.log_date)
        
        # Create EmployeePayment records
        created_count = 0
        for (employee_id, payment_date), data in payment_data.items():
            # Check if payment record already exists
            existing = EmployeePayment.query.filter_by(
                employee_id=employee_id,
                payment_date=payment_date
            ).first()
            
            if not existing:
                new_payment = EmployeePayment(
                    employee_id=employee_id,
                    total_trips=data['total_trips'],
                    total_fare_collected=data['total_fare_collected'],
                    commission_earned=data['commission_earned'],
                    payment_status='completed',
                    payment_date=payment_date
                )
                
                db.session.add(new_payment)
                created_count += 1
                
                # Get employee name for logging
                employee = User.query.get(employee_id)
                employee_name = employee.get_full_name() if employee else f"ID:{employee_id}"
                
                print(f"✅ Created payment for {employee_name} on {payment_date}: "
                      f"Trips={data['total_trips']}, "
                      f"Fare=KES{data['total_fare_collected']:,.2f}, "
                      f"Commission=KES{data['commission_earned']:,.2f}")
        
        # Commit all changes
        if created_count > 0:
            db.session.commit()
            print(f"🎉 Successfully created {created_count} EmployeePayment records!")
        else:
            print("ℹ️  No new payment records needed - all data already exists")
        
        # Verify the results
        total_payments = EmployeePayment.query.count()
        print(f"📊 Total EmployeePayment records in database: {total_payments}")
        
        # Show sample of created records
        sample_payments = EmployeePayment.query.limit(5).all()
        if sample_payments:
            print("\n📋 Sample payment records:")
            for payment in sample_payments:
                employee = User.query.get(payment.employee_id)
                employee_name = employee.get_full_name() if employee else f"ID:{payment.employee_id}"
                print(f"  • {employee_name}: {payment.payment_date} - "
                      f"Trips: {payment.total_trips}, "
                      f"Fare: KES{payment.total_fare_collected:,.2f}, "
                      f"Commission: KES{payment.commission_earned:,.2f}")

if __name__ == "__main__":
    populate_employee_payments()