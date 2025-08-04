# Fleet and Route Management - Code Documentation

## **Fleet Model** ([`server/models/fleet.py`](server/models/fleet.py:1))

```python
from config import db
from datetime import datetime

class Fleet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plate_number = db.Column(db.String(20), nullable=False, unique=True)
    vehicle_model = db.Column(db.String(100), nullable=False)
    assigned_route = db.Column(db.String(100))
    status = db.Column(db.String(50), default='active')
```

## **Route Assignment Model** ([`server/models/route_assignment.py`](server/models/route_assignment.py:1))

```python
from config import db
from datetime import datetime

class AssignedRoute(db.Model):
    __tablename__ = 'assigned_route'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=True)
    date_assigned = db.Column(db.DateTime, default=datetime.utcnow)
    start_date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    end_date = db.Column(db.Date, nullable=True)
    
    # Assignment status: 'active', 'completed', 'cancelled'
    status = db.Column(db.String(20), nullable=False, default='active')
    
    # Additional metadata
    shift = db.Column(db.String(20), nullable=True)  # 'morning', 'afternoon', 'evening'
    notes = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    employee = db.relationship('User', foreign_keys=[employee_id], backref='assignments')
    route = db.relationship('Route', backref='assigned_routes')
    vehicle = db.relationship('Vehicle', backref='route_assignments')
    admin = db.relationship('User', foreign_keys=[created_by], backref='created_assignments')
    
    def __repr__(self):
        return f"AssignedRoute(id={self.id}, employee_id={self.employee_id}, route_id={self.route_id}, vehicle_id={self.vehicle_id}, status={self.status})"
```

## **Route Model** ([`server/models/route.py`](server/models/route.py:1))

```python
from config import db

class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    route_name = db.Column(db.String(100), nullable=False)
    origin = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    stops = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), nullable=False)
```

## **Fleet Management Backend Routes** ([`run.py`](run.py:461))

```python
@app.route('/admin/fleet')
@login_required
def fleet_management():
    fleet_vehicles = Fleet.query.all()
    return render_template('admin/FleetManagement.html', fleet_vehicles=fleet_vehicles)

@app.route('/admin/fleet/add', methods=['POST'])
def add_fleet():
    plate = request.form.get("plate_number")
    model = request.form.get("vehicle_model")
    route = request.form.get("assigned_route")
    status = request.form.get("status")

    new_vehicle = Fleet(
        plate_number=plate,
        vehicle_model=model,
        assigned_route=route,
        status=status
    )
    db.session.add(new_vehicle)
    db.session.commit()

    flash("Vehicle added successfully!")
    return redirect(url_for('fleet_management'))
```

## **Route Management Backend Routes** ([`run.py`](run.py:486))

```python
@app.route('/admin/routes')
@login_required
def manage_routes():
    routes = Route.query.all()
    return render_template('admin/ManageRoute.html', routes=routes)

@app.route('/admin/routes/add', methods=['POST'])
@login_required
def add_route():
    route_name = request.form.get("route_name")
    origin = request.form.get("origin")
    destination = request.form.get("destination")
    stops = request.form.get("stops")
    status = request.form.get("status")

    new_route = Route(
        route_name=route_name,
        origin=origin,
        destination=destination,
        stops=stops,
        status=status
    )
    db.session.add(new_route)
    db.session.commit()

    flash("Route added successfully!")
    return redirect(url_for('manage_routes'))
```

## **Route Assignment Backend Routes** ([`run.py`](run.py:1223))

```python
@app.route('/admin/route-assignment', methods=['GET'])
@login_required
def route_assignment():
    if current_user.role != 'admin':
        flash("Unauthorized access", "error")
        return redirect(url_for('login'))
    
    # Get filter parameters
    driver_id = request.args.get('driver', 'all')
    route_id = request.args.get('route', 'all')
    status = request.args.get('status', 'all')
    
    # Base query
    query = AssignedRoute.query
    
    # Apply filters
    if driver_id != 'all':
        query = query.filter(AssignedRoute.employee_id == driver_id)
    if route_id != 'all':
        query = query.filter(AssignedRoute.route_id == route_id)
    if status != 'all':
        query = query.filter(AssignedRoute.status == status)
    
    # Get assignments with filters applied
    assignments = query.order_by(AssignedRoute.date_assigned.desc()).all()
    
    # Get drivers, routes, and vehicles for the form
    drivers = User.query.filter_by(role='employee').all()
    routes = Route.query.filter_by(status='active').all()
    vehicles = Fleet.query.all()
    
    return render_template(
        'admin/route_assignment.html',
        assignments=assignments,
        drivers=drivers,
        routes=routes,
        vehicles=vehicles
    )

@app.route('/admin/route-assignment/add', methods=['POST'])
@login_required
def add_route_assignment():
    if current_user.role != 'admin':
        flash("Unauthorized access", "error")
        return redirect(url_for('login'))
    
    # Get form data
    employee_id = request.form.get('employee_id')
    route_id = request.form.get('route_id')
    vehicle_id = request.form.get('vehicle_id') or None
    start_date_str = request.form.get('start_date')
    end_date_str = request.form.get('end_date')
    shift = request.form.get('shift')
    notes = request.form.get('notes')
    
    # Convert dates
    from datetime import datetime
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
    
    # Create new assignment
    new_assignment = AssignedRoute(
        employee_id=employee_id,
        route_id=route_id,
        vehicle_id=vehicle_id,
        start_date=start_date,
        end_date=end_date,
        shift=shift,
        notes=notes,
        status='active',
        created_by=current_user.id
    )
    
    db.session.add(new_assignment)
    db.session.commit()
    
    flash("Route assigned successfully!", "success")
    return redirect(url_for('route_assignment'))

@app.route('/admin/route-assignment/edit/<int:assignment_id>', methods=['GET', 'POST'])
@login_required
def edit_route_assignment(assignment_id):
    if current_user.role != 'admin':
        flash("Unauthorized access", "error")
        return redirect(url_for('login'))
    
    # Get the assignment
    assignment = AssignedRoute.query.get_or_404(assignment_id)
    
    if request.method == 'POST':
        # Update assignment with form data
        assignment.employee_id = request.form.get('employee_id')
        assignment.route_id = request.form.get('route_id')
        assignment.vehicle_id = request.form.get('vehicle_id') or None
        
        # Convert dates
        from datetime import datetime
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        assignment.start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
        assignment.end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
        
        assignment.shift = request.form.get('shift')
        assignment.notes = request.form.get('notes')
        assignment.status = request.form.get('status')
        assignment.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        flash("Assignment updated successfully!", "success")
        return redirect(url_for('route_assignment'))
    
    # Get data for form
    drivers = User.query.filter_by(role='employee').all()
    routes = Route.query.all()
    vehicles = Fleet.query.all()
    
    return render_template(
        'admin/edit_route_assignment.html',
        assignment=assignment,
        drivers=drivers,
        routes=routes,
        vehicles=vehicles
    )

@app.route('/admin/route-assignment/delete/<int:assignment_id>')
@login_required
def delete_route_assignment(assignment_id):
    if current_user.role != 'admin':
        flash("Unauthorized access", "error")
        return redirect(url_for('login'))
    
    assignment = AssignedRoute.query.get_or_404(assignment_id)
    db.session.delete(assignment)
    db.session.commit()
    
    flash("Assignment deleted successfully!", "success")
    return redirect(url_for('route_assignment'))
```

## **Fleet Management Frontend** ([`templates/admin/FleetManagement.html`](templates/admin/FleetManagement.html:198))

```html
<!-- Add Vehicle Form -->
<form id="addFleetForm" style="display:none;" method="POST" action="/admin/fleet/add">
  <input type="text" name="plate_number" placeholder="Plate Number (e.g. KDA 123A)" required>
  <input type="text" name="vehicle_model" placeholder="Vehicle Model (e.g. Nissan Caravan)" required>
  <input type="text" name="assigned_route" placeholder="Assigned Route (e.g. CBD - Rongai)" required>
  <select name="status">
    <option value="active">Active</option>
    <option value="inactive">Inactive</option>
  </select>
  <button type="submit">Save Vehicle</button>
</form>

<!-- Fleet Table -->
<table class="route-table">
  <thead>
    <tr>
      <th>Plate No.</th>
      <th>Model</th>
      <th>Route</th>
      <th>Status</th>
      <th>Actions</th>
    </tr>
  </thead>
  <tbody>
    {% for vehicle in fleet_vehicles %}
    <tr>
      <td>{{ vehicle.plate_number }}</td>
      <td>{{ vehicle.vehicle_model }}</td>
      <td>{{ vehicle.assigned_route }}</td>
      <td><span class="badge {{ 'active' if vehicle.status == 'active' else 'inactive' }}">{{ vehicle.status|title }}</span></td>
      <td>
        <button class="edit-btn">Edit</button>
        <button class="delete-btn">Delete</button>
      </td>
    </tr>
    {% endfor %}
  </tbody>
</table>

<script>
  function toggleForm() {
    const form = document.getElementById('addFleetForm');
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
  }
</script>
```

## **Route Management Frontend** ([`templates/admin/ManageRoute.html`](templates/admin/ManageRoute.html:207))

```html
<!-- Add Route Form -->
<form id="addRouteForm" style="display:none;" method="POST" action="/admin/routes/add">
  <input type="text" name="route_name" placeholder="Route Name (e.g., CBD – Rongai)" required>
  <input type="text" name="origin" placeholder="Origin (e.g., CBD)" required>
  <input type="text" name="destination" placeholder="Destination (e.g., Rongai)" required>
  <input type="text" name="stops" placeholder="Key Stops (comma-separated)" required>
  <select name="status">
    <option value="active">Active</option>
    <option value="inactive">Inactive</option>
  </select>
  <button type="submit">Save Route</button>
</form>

<!-- Routes Table -->
<table class="route-table">
  <thead>
    <tr>
      <th>Route</th>
      <th>Origin</th>
      <th>Destination</th>
      <th>Stops</th>
      <th>Status</th>
      <th>Actions</th>
    </tr>
  </thead>
  <tbody>
  {% for route in routes %}
    <tr>
      <td>{{ route.route_name }}</td>
      <td>{{ route.origin }}</td>
      <td>{{ route.destination }}</td>
      <td>{{ route.stops }}</td>
      <td>
        {% if route.status == 'active' %}
        <span class="badge active">Active</span>
        {% else %}
        <span class="badge">Inactive</span>
        {% endif %}
      </td>
      <td>
        <button class="edit-btn">Edit</button>
        <button class="delete-btn">Delete</button>
      </td>
    </tr>
  {% endfor %}
  </tbody>
</table>

<script>
  function toggleForm() {
    const form = document.getElementById('addRouteForm');
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
  }
</script>
```

## **System Architecture Summary**

### **Database Models**
- **[`Fleet`](server/models/fleet.py:4)**: Vehicle management with plate numbers, models, and status
- **[`Route`](server/models/route.py:3)**: Route definitions with origins, destinations, and stops
- **[`AssignedRoute`](server/models/route_assignment.py:4)**: Links employees to routes with scheduling and vehicle assignment

### **Key Features**
- **Fleet Registration**: Add/manage vehicles with unique plate numbers
- **Route Management**: Create and manage transport routes
- **Route Assignment**: Assign employees to specific routes with vehicles and shifts
- **Status Tracking**: Active/inactive status for vehicles and routes
- **Scheduling**: Start/end dates and shift management for assignments
- **Admin Controls**: Full CRUD operations for fleet and route management

### **Integration Points**
- **User Management**: Links to [`User`](server/models/user.py:8) model for employee assignments
- **Vehicle Health**: Integration with [`VehicleHealth`](server/models/vehicle_health.py:4) for maintenance tracking
- **Performance Tracking**: Links to [`Performance`](server/models/performance.py:6) model for route performance
- **Driver Logs**: Integration with [`DriverLog`](server/models/driver_log.py:4) for daily operations