from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://neondb_owner:npg_Ppi40tyhJXqM@ep-falling-sound-a5vutgze-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# models filezz
class Property(db.Model):
    __tablename__ = 'properties'
    PropertyID = db.Column(db.Integer, primary_key=True)
    Address = db.Column(db.String(255))
    City = db.Column(db.String(100))
    State = db.Column(db.String(50))
    ZipCode = db.Column(db.String(20))
    PropertyType = db.Column(db.String(50))
    NumberOfRooms = db.Column(db.Integer)
    RentAmount = db.Column(db.Float)
    Status = db.Column(db.String(50))

class Tenant(db.Model):
    __tablename__ = 'tenants'
    TenantID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(100))
    LastName = db.Column(db.String(100))
    PhoneNumber = db.Column(db.String(20))
    EmailAddress = db.Column(db.String(100))
    LeaseStartDate = db.Column(db.Date)
    LeaseEndDate = db.Column(db.Date)
    PropertyID = db.Column(db.Integer, db.ForeignKey('properties.PropertyID'))

class Payment(db.Model):
    __tablename__ = 'payments'
    PaymentID = db.Column(db.Integer, primary_key=True)
    TenantID = db.Column(db.Integer, db.ForeignKey('tenants.TenantID'))
    PaymentDate = db.Column(db.Date)
    Amount = db.Column(db.Float)
    PaymentMethod = db.Column(db.String(50))
    Status = db.Column(db.String(50))

class MaintenanceRequest(db.Model):
    __tablename__ = 'maintenancerequests'
    RequestID = db.Column(db.Integer, primary_key=True)
    PropertyID = db.Column(db.Integer, db.ForeignKey('properties.PropertyID'))
    TenantID = db.Column(db.Integer, db.ForeignKey('tenants.TenantID'))
    RequestDate = db.Column(db.Date)
    Description = db.Column(db.Text)
    Status = db.Column(db.String(50))
    CompletionDate = db.Column(db.Date, nullable=True)

class LeaseAgreement(db.Model):
    __tablename__ = 'leaseagreements'
    LeaseID = db.Column(db.Integer, primary_key=True)
    PropertyID = db.Column(db.Integer, db.ForeignKey('properties.PropertyID'))
    TenantID = db.Column(db.Integer, db.ForeignKey('tenants.TenantID'))
    LeaseStartDate = db.Column(db.Date)
    LeaseEndDate = db.Column(db.Date)
    MonthlyRentAmount = db.Column(db.Float)
    SecurityDepositAmount = db.Column(db.Float)

# Routeszzz
@app.route('/')
def index():
    properties = Property.query.all()
    tenants = Tenant.query.all()
    payments = Payment.query.all()
    requests = MaintenanceRequest.query.all()
    leases = LeaseAgreement.query.all()
    return render_template('index.html', properties=properties, tenants=tenants, payments=payments, requests=requests, leases=leases)

@app.route('/add_property', methods=['GET', 'POST'])
def add_property():
    if request.method == 'POST':
        new_property = Property(
            Address=request.form['address'],
            City=request.form['city'],
            State=request.form['state'],
            ZipCode=request.form['zip_code'],
            PropertyType=request.form['property_type'],
            NumberOfRooms=request.form['rooms'],
            RentAmount=request.form['rent'],
            Status=request.form['status']
        )
        db.session.add(new_property)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('add_property.html')

@app.route('/add_tenant', methods=['GET', 'POST'])
def add_tenant():
    if request.method == 'POST':
        new_tenant = Tenant(
            FirstName=request.form['first_name'],
            LastName=request.form['last_name'],
            PhoneNumber=request.form['phone'],
            EmailAddress=request.form['email'],
            LeaseStartDate=request.form['lease_start'],
            LeaseEndDate=request.form['lease_end'],
            PropertyID=request.form['property_id']
        )
        db.session.add(new_tenant)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_tenant.html')

@app.route('/delete_tenant/<int:tenant_id>')
def delete_tenant(tenant_id):
    tenant_to_delete = Tenant.query.get_or_404(tenant_id)
    db.session.delete(tenant_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_payment', methods=['GET', 'POST'])
def add_payment():
    if request.method == 'POST':
        new_payment = Payment(
            TenantID=request.form['tenant_id'],
            PaymentDate=request.form['payment_date'],
            Amount=request.form['amount'],
            PaymentMethod=request.form['method'],
            Status=request.form['status']
        )
        db.session.add(new_payment)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_payment.html')

@app.route('/delete_payment/<int:payment_id>')
def delete_payment(payment_id):
    payment_to_delete = Payment.query.get_or_404(payment_id)
    db.session.delete(payment_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_request', methods=['GET', 'POST'])
def add_request():
    if request.method == 'POST':
        new_request = MaintenanceRequest(
            PropertyID=request.form['property_id'],
            TenantID=request.form['tenant_id'],
            RequestDate=request.form['request_date'],
            Description=request.form['description'],
            Status=request.form['status']
        )
        db.session.add(new_request)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_request.html')

@app.route('/delete_request/<int:request_id>')
def delete_request(request_id):
    request_to_delete = MaintenanceRequest.query.get_or_404(request_id)
    db.session.delete(request_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_lease', methods=['GET', 'POST'])
def add_lease():
    if request.method == 'POST':
        new_lease = LeaseAgreement(
            PropertyID=request.form['property_id'],
            TenantID=request.form['tenant_id'],
            LeaseStartDate=request.form['lease_start'],
            LeaseEndDate=request.form['lease_end'],
            MonthlyRentAmount=request.form['rent_amount'],
            SecurityDepositAmount=request.form['deposit']
        )
        db.session.add(new_lease)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_lease.html')

@app.route('/delete_lease/<int:lease_id>')
def delete_lease(lease_id):
    lease_to_delete = LeaseAgreement.query.get_or_404(lease_id)
    db.session.delete(lease_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
