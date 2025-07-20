from config import db

class EmployeePayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    total_trips = db.Column(db.Integer)
    total_fare_collected = db.Column(db.Float)
    commission_earned = db.Column(db.Float)
    payment_status = db.Column(db.String(20))
    payment_date = db.Column(db.Date)

    employee = db.relationship('User', backref='employee_payments')