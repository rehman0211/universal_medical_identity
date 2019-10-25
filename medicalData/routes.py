import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from datetime import datetime
from medicalData import app, db, bcrypt, mail
from medicalData.forms import (RegistrationForm, LoginForm, PatientForm, DoctorForm, InsuranceCompanyForm, UpdateAccountForm,
                                 RequestResetForm, ResetPasswordForm,)
from medicalData.models import User, Patient, Doctor, InsuranceCompany, GovernmentBody,Report, Appointment, Disease
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import pickle
import numpy as np

loaded_model = pickle.load(open("medicalData\model.sav","rb"))

symptoms_dict = {
    "abdominal_pain": 39,
    "abnormal_menstruation": 101,
    "acidity": 8,
    "acute_liver_failure": 44,
    "altered_sensorium": 98,
    "anxiety": 16,
    "back_pain": 37,
    "belly_pain": 100,
    "blackheads": 123,
    "bladder_discomfort": 89,
    "blister": 129,
    "blood_in_sputum": 118,
    "bloody_stool": 61,
    "blurred_and_distorted_vision": 49,
    "breathlessness": 27,
    "brittle_nails": 72,
    "bruising": 66,
    "burning_micturition": 12,
    "chest_pain": 56,
    "chills": 5,
    "cold_hands_and_feets": 17,
    "coma": 113,
    "congestion": 55,
    "constipation": 38,
    "continuous_feel_of_urine": 91,
    "continuous_sneezing": 3,
    "cough": 24,
    "cramps": 65,
    "dark_urine": 33,
    "dehydration": 29,
    "depression": 95,
    "diarrhoea": 40,
    "dischromic _patches": 102,
    "distention_of_abdomen": 115,
    "dizziness": 64,
    "drying_and_tingling_lips": 76,
    "enlarged_thyroid": 71,
    "excessive_hunger": 74,
    "extra_marital_contacts": 75,
    "family_history": 106,
    "fast_heart_rate": 58,
    "fatigue": 14,
    "fluid_overload": 45,
    "fluid_overload.1": 117,
    "foul_smell_of urine": 90,
    "headache": 31,
    "high_fever": 25,
    "hip_joint_pain": 79,
    "history_of_alcohol_consumption": 116,
    "increased_appetite": 104,
    "indigestion": 30,
    "inflammatory_nails": 128,
    "internal_itching": 93,
    "irregular_sugar_level": 23,
    "irritability": 96,
    "irritation_in_anus": 62,
    "itching": 0,
    "joint_pain": 6,
    "knee_pain": 78,
    "lack_of_concentration": 109,
    "lethargy": 21,
    "loss_of_appetite": 35,
    "loss_of_balance": 85,
    "loss_of_smell": 88,
    "malaise": 48,
    "mild_fever": 41,
    "mood_swings": 18,
    "movement_stiffness": 83,
    "mucoid_sputum": 107,
    "muscle_pain": 97,
    "muscle_wasting": 10,
    "muscle_weakness": 80,
    "nausea": 34,
    "neck_pain": 63,
    "nodal_skin_eruptions": 2,
    "obesity": 67,
    "pain_behind_the_eyes": 36,
    "pain_during_bowel_movements": 59,
    "pain_in_anal_region": 60,
    "painful_walking": 121,
    "palpitations": 120,
    "passage_of_gases": 92,
    "patches_in_throat": 22,
    "phlegm": 50,
    "polyuria": 105,
    "prominent_veins_on_calf": 119,
    "puffy_face_and_eyes": 70,
    "pus_filled_pimples": 122,
    "receiving_blood_transfusion": 111,
    "receiving_unsterile_injections": 112,
    "red_sore_around_nose": 130,
    "red_spots_over_body": 99,
    "redness_of_eyes": 52,
    "restlessness": 20,
    "runny_nose": 54,
    "rusty_sputum": 108,
    "scurring": 124,
    "shivering": 4,
    "silver_like_dusting": 126,
    "sinus_pressure": 53,
    "skin_peeling": 125,
    "skin_rash": 1,
    "slurred_speech": 77,
    "small_dents_in_nails": 127,
    "spinning_movements": 84,
    "spotting_ urination": 13,
    "stiff_neck": 81,
    "stomach_bleeding": 114,
    "stomach_pain": 7,
    "sunken_eyes": 26,
    "sweating": 28,
    "swelled_lymph_nodes": 47,
    "swelling_joints": 82,
    "swelling_of_stomach": 46,
    "swollen_blood_vessels": 69,
    "swollen_extremeties": 73,
    "swollen_legs": 68,
    "throat_irritation": 51,
    "toxic_look_(typhos)": 94,
    "ulcers_on_tongue": 9,
    "unsteadiness": 86,
    "visual_disturbances": 110,
    "vomiting": 11,
    "watering_from_eyes": 103,
    "weakness_in_limbs": 57,
    "weakness_of_one_body_side": 87,
    "weight_gain": 15,
    "weight_loss": 19,
    "yellow_crust_ooze": 131,
    "yellow_urine": 42,
    "yellowing_of_eyes": 43,
    "yellowish_skin": 32,
}

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/patient_info_update", methods=['GET', 'POST'])
def patient_info_update():
    if request.method == 'POST':
      f =request.files['pic']
      patient_info= Patient(user_id=1,fullName=request.form['fullname'],qr_code='nnjhbhj',phoneNo=request.form['phoneNumber'],city=request.form['districtName'],state=request.form['stateName'],image_file=f.read(),current_doctorId=2)
      db.session.add(patient_info)
      db.session.commit()  
      return redirect('dashboard')
    return render_template('patient_next.html')

@app.route("/dashboard_patient")
def dashboard_patient():
    return render_template('dashboard_patient.html')
@app.route("/dashboard_doctor")
def dashboard_doctor():
    return render_template('dashboard_doctor.html')
@app.route("/patient_history",methods=['GET', 'POST'])
def patient_history():
    if request.method == 'POST':
        tag=request.form['tag']
        input_vector = np.zeros(len(symptoms_dict))
        symp = symptoms_dict[tag]
        input_vector[symp]=1
        prediction=loaded_model.predict([input_vector])[0]
        # appointments=Appointment.query.filter_by(Appointment.disease.tag=tag).second()
        return render_template('patient_history.html',prediction=prediction) 
    return render_template('patient_history.html')
@app.route("/search")
def search():
    return render_template('search.html')       
# @app.route("/dashboard_patient")
# def dashboard_patient():
#     return render_template('dashboard_patient.html')
# @app.route("/dashboard_patient")
# def dashboard_patient():
#     return render_template('dashboard_patient.html')   
# @app.route("/patient_histroy")
# def patient_history():
#     return render_template('patient_history.html')          
       

@app.route('/handle_data', methods=['POST'])
def handle_data():
    return render_template('forgot_password.html')    


@app.route('/forgotpassword_form', methods=['GET', 'POST'])
def forgotpassword_form():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))

    # show the form, it wasn't submitted
    return render_template('forgot_password.html')    

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/login", methods=['GET', 'POST'])
def login():
    user=User.query.filter_by(username=request.form['username']).first()
    # hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
    if user:
        if bcrypt.check_password_hash(user.password,request.form['password']):
            return redirect(url_for('patient_history'))
    flash('Your account has been created! You are now able to log in', 'success')         
    return redirect(url_for('home'))
# @app.route("/getAppointmentsByUser",method=['POST'])
# def getAppointmentsByUser():
#     if request.method == 'POST':
#         tag=req.body['tag']
#         input_vector = np.zeros(len(symptoms_dict))
#         symp = symptoms_dict[tag]
#         input_vector[symp]=1
#         prediction=loaded_model.predict([input_vector])[0]
#         # appointments=Appointment.query.filter_by(Appointment.disease.tag=tag).second()
#         return render_template('patient_history.html',prediction=prediction)    
#     return render_template('patient_dashboard.html')    
    # uname=request.form['username']
    # Email=request.form['useremail']
    # uType=request.form['userType']
    # user = User(username=uname, email=Email, password=hashed_password,userType=uType)
    # db.session.add(user)
    # db.session.commit()
    # flash('Your account has been created! You are now able to log in', 'success')
    return redirect(url_for('patient_info_update'))    


@app.route("/register", methods=['GET', 'POST'])
def register():
    hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
    uname=request.form['username']
    Email=request.form['useremail']
    uType=request.form['userType']
    user = User(username=uname, email=Email, password=hashed_password,userType=uType)
    db.session.add(user)
    db.session.commit()
    flash('Your account has been created! You are now able to log in', 'success')
    return redirect(url_for('dashboard_patient'))
   #  if current_user.is_authenticated:
   #      return redirect(url_for('home'))
   #  form = RegistrationForm()
   #  if form.validate_on_submit():
   #      hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
   #      user = User(username=request.form['username'], email=request.form['useremail'], password=hashed_password,userType=request.form['userType'],lastLogin=datatime.utcnow)
   #      db.session.add(user)
   #      db.session.commit()
   #      flash('Your account has been created! You are now able to log in', 'success')
   #      return redirect(url_for('home'))
   # # return render_template('patient_next.html', title='Register', form=form)
   #  return render_template('forgot_password.html')


# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user and bcrypt.check_password_hash(user.password, form.password.data):
#             login_user(user, remember=form.remember.data)
#             next_page = request.args.get('next')
#             return redirect(next_page) if next_page else redirect(url_for('home'))
#         else:
#             flash('Login Unsuccessful. Please check email and password', 'danger')
#     return render_template('login.html', title='Login', form=form)
  


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)







    # public static String generatePIN() {
    #     int randomPIN = (int) (Math.random() * 900000) + 100000;
    #     return "" + randomPIN;
    # }