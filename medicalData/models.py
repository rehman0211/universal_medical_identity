from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from medicalData import db, login_manager, app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



#user
#patient
#doctor
#insurance company
#government body

#Report
#appointment



patient_doctor = db.table('patient_doctor',
    db.Column('patient_id',db.Integer,db.ForeignKey('patient.id')),
    db.Column('doctor_id',db.Integer,db.ForeignKey('doctor.id'))
)
patient_disease = db.table('patient_desiese',
    db.Column('patient_id',db.Integer,db.ForeignKey('patient.id')),
    db.Column('disease',db.Integer,db.ForeignKey('disease.id'))
)
patient_report = db.table('patient_report',
    db.Column('patient_id',db.Integer,db.ForeignKey('patient.id')),
    db.Column('report_id',db.Integer,db.ForeignKey('report.id'))
)
patient_appointment = db.table('patient_appointment',
    db.Column('patient_id',db.Integer,db.ForeignKey('patient.id')),
    db.Column('appointment_id',db.Integer,db.ForeignKey('appointment.id'))
)
doctor_report = db.table('doctor_report',
    db.Column('doctor_id',db.Integer,db.ForeignKey('doctor.id')),
    db.Column('report_id',db.Integer,db.ForeignKey('report.id'))
)
doctor_appointment = db.table('doctor_appointment',
    db.Column('doctor_id',db.Integer,db.ForeignKey('doctor.id')),
    db.Column('appointment_id',db.Integer,db.ForeignKey('appointment.id'))
)
disease_appointment = db.table('disease_appointment',
    db.Column('disease_id',db.Integer,db.ForeignKey('disease.id')),
    db.Column('appointment_id',db.Integer,db.ForeignKey('appointment.id'))
)



                                    ###############

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    userType = db.Column(db.String(60), nullable=False)
    lastLogin = db.Column(db.DateTime, nullable = True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.id}', '{self.email}', '{self.image_file}')"


                                    ###############

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    fullName = db.Column(db.String(60),nullable=False)
    qr_code = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.DateTime, nullable=False)
    phoneNo = db.Column(db.String(12), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    city = db.Column(db.String(20), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    current_doctorId = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    #insuranceCompany_id = db.Column(db.Integer ,db.ForeignKey('insuranceCompany.id'),nullable=True)
    doctors = db.relationship('Doctor',secondary=patient_doctor, backref=db.backref('patient',lazy='dynamic'))#many to many
    diseases = db.relationship('Disease',secondary=patient_disease, backref=db.backref('patient',lazy='dynamic'))#many to many
    reports = db.relationship('Report', secondary=patient_report, backref=db.backref('patient',lazy='dynamic'))#many to many
    appointments = db.relationship('Appointment', secondary=patient_appointment, backref=db.backref('patient',lazy='dynamic'))#many to many

    def __repr__(self):
        return f"User('{self.id}')"


                                    ###############

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    fullName = db.Column(db.String(60),nullable=False)
    licenceNo = db.Column(db.String(20), nullable=False)
    speciality = db.Column(db.String(40), nullable=False)
    department = db.Column(db.String(40), nullable=False)
    hospitalName = db.Column(db.String(40), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    current_patientId = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    reports = db.relationship('Report', secondary=doctor_report, backref=db.backref('doctor',lazy='dynamic'))#many to many
    appointments = db.relationship('Appointment', secondary=doctor_appointment, backref=db.backref('doctor',lazy='dynamic'))#many to many



    def __repr__(self):
        return f"User('{self.id}')"

                                    ###############

class InsuranceCompany(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullName = db.Column(db.String(60),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    licenceNo = db.Column(db.String(20), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    def __repr__(self):
        return f"User('{self.id}')"

                                    ###############

class GovernmentBody(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    def __repr__(self):
        return f"User('{self.id}')"


                                    ###############

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)


    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.id}')"

                                    ###############

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)#many to many
    report = db.Column(db.Integer, db.ForeignKey('report.id'), nullable=False)#one to one
    disease = db.relationship('Disease', secondary=disease_appointment, backref=db.backref('appointment',lazy='dynamic'))#many to many
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.id}')"

                                    ###################

class Disease(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(40), nullable=False)
    department = db.Column(db.String(40), nullable=False)
        
    def __repr__(self):
        return f"User('{self.id}')"


