from flask import Flask,render_template,request,redirect,url_for,flash,session
from models import db,User,Professional,Admin,Service,Service_Request,Service_Status
from flask_login import LoginManager,login_user,login_required,current_user,logout_user
from flask_mail import Mail,Message
from flask_socketio import SocketIO,emit
from werkzeug.utils import secure_filename

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///app.db"
app.config["SECRET_KEY"]="#bfkfabwksj%1212"
db.init_app(app)

#Login
login_manager = LoginManager()
login_manager.init_app(app)
# login_manager.login_view='login'

#Email
app.config["MAIL_SERVER"]="smtp.gmail.com"
app.config["MAIL_PORT"]=465
app.config["MAIL_USE_TTL"]=False
app.config["MAIL_USE_SSL"]=True
app.config["MAIL_USERNAME"]="ayushgame2910@gmail.com"
app.config["MAIL_PASSWORD"]="xfgb tsef ytli mrih"
mail=Mail(app)

socketio=SocketIO(app)

UPLOAD_FOLDER='static/uploads'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
ALLOWED_EXTENSIONS={'png','jpeg','jpg'}

# Function to check file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@login_manager.user_loader
def load_user(user_id):
    parts=str(user_id).split("-")
    if len(parts)!=2:
        return None
    user_type,user_id=parts
    if user_type=="user":
        return User.query.get(int(user_id))
    elif user_type=="prof":
        return Professional.query.get(int(user_id))
    elif user_type=="admin":
        return Admin.query.get(int(user_id))
    else:
        return None

@app.route("/ulogout")
@login_required
def u_logout():
    session.clear()
    logout_user()
    flash("Logged out!")
    return redirect(url_for("user_login"))

@app.route("/plogout")
@login_required
def p_logout():
    session.clear()
    logout_user()
    flash("Logged out!")
    return redirect(url_for("professional_login"))

@app.route("/alogout")
@login_required
def a_logout():
    session.clear()
    logout_user()
    flash("Logged out!")
    return redirect(url_for("admin_login"))

# with app.app_context():
#     db.create_all()

@app.route('/')
def index():
    return render_template("Login Page.html")

@app.route('/ulogin',methods=["GET","POST"])
def user_login():
    if request.method=="GET":
        return render_template("User_Login.html")
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["pwd"]

        user = User.query.filter_by(u_email=email).first()

        if user and user.u_pwd==password:
            login_user(user)
            flash("Login Successful!")
            return redirect(url_for("uprofile"))

        flash("Invalid username or password!")

    return render_template("User_Login.html")

@app.route('/plogin',methods=["GET","POST"])
def professional_login():
    if request.method=="GET":
        return render_template("Professional_Login.html")
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["pwd"]

        professional = Professional.query.filter_by(p_email=email).first()

        if professional and professional.p_pwd==password:
            login_user(professional)
            flash("Login Successful!")
            return redirect(url_for("pprofile"))

        flash("Invalid username or password!")

    return render_template("Professional_Login.html")

@app.route('/alogin',methods=["GET","POST"])
def admin_login():
    if request.method=="GET":
        return render_template("Admin_Login.html")
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["pwd"]

        admin = Admin.query.filter_by(a_email=email).first()

        if admin and admin.a_pwd==password:
            login_user(admin)
            flash("Login Successful!")
            return redirect(url_for("admin"))

        flash("Invalid username or password!")

    return render_template("Admin_Login.html")

@app.route('/uregister',methods=["GET","POST"])
def user_register():
    if request.method=="GET":
        return render_template("User_Register.html")
    if request.method=="POST":
        try:
            f_name=request.form["f_name"]
            l_name=request.form["l_name"]
            email=request.form["email"]
            phoneno=request.form["phoneno"]
            pwd=request.form["pwd"]

            with app.app_context():
                new_user=User(u_f_name=f_name,u_l_name=l_name,u_phoneno=phoneno,u_pwd=pwd,u_email=email)
                db.session.add(new_user)
                db.session.commit()
            flash("Registration successful!")
            return redirect(url_for("user_login"))
        except:
            flash("Registration unsuccessful!")
            return redirect(url_for("user_register"))

@app.route('/pregister',methods=["GET","POST"])
def professional_register():
    if request.method=="GET":
        return render_template("Professional_Register.html")
    if request.method=="POST":
        try:
            f_name=request.form["f_name"]
            l_name=request.form["l_name"]
            email=request.form["email"]
            phoneno=request.form["phoneno"]
            pwd=request.form["pwd"]

            with app.app_context():
                new_professional=Professional(p_f_name=f_name,p_l_name=l_name,p_phoneno=phoneno,p_pwd=pwd,p_email=email)
                db.session.add(new_professional)
                db.session.commit()
            flash("Registration successful!")
            return redirect(url_for("professional_login"))
        except:
            flash("Registration unsuccessful!")
            return redirect(url_for("professional_register"))

@app.route('/uprofile')
@login_required
def uprofile():
    return render_template("U_Profile.html",user=current_user)

@app.route('/pprofile')
@login_required
def pprofile():
    return render_template("P_Profile.html",professional=current_user)

@app.route('/admin',methods=["GET","POST"])
@login_required
def admin():
    try:
        users = User.query.all()
        professionals = Professional.query.all()
        return render_template("admin.html", users=users, professionals=professionals)
    except:
        print("admin login exception")
        return redirect(url_for("admin_login"))

@app.route('/admin/block/<string:s>/<int:i>',methods=["GET","POST"])
@login_required
def admin_block(s,i):
    if request.method=="GET":
        try:
            if s=='user':
                try:
                    flash("User Blocked",'User Blocked')
                    block_user=User.query.filter_by(u_id=i).first()
                    if block_user.isBlock==False:
                        block_user.isBlock=True
                        db.session.commit()
                    else:
                        block_user.isBlock = False
                        db.session.commit()
                    db.session.commit()
                    return redirect(url_for('admin'))
                except:
                    return redirect(url_for('admin'))
            if s=='professional':
                try:
                    flash("Professional Blocked",'Professional Blocked')
                    block_professional = Professional.query.filter_by(p_id=i).first()
                    if block_professional.isBlock==False:
                        block_professional.isBlock = True
                        db.session.commit()
                    else:
                        block_professional.isBlock = False
                        db.session.commit()
                    return redirect(url_for('admin'))
                except:
                    return redirect(url_for('admin'))
        except:
            return redirect(url_for('admin'))

@app.route('/admin/approve/<string:s>/<int:i>',methods=["GET","POST"])
@login_required
def admin_approve_professional(s,i):
    if s == 'professional':
        try:
            try:
                flash("Professional Blocked", 'Professional Blocked')
                block_professional = Professional.query.filter_by(p_id=i).first()
                if block_professional.isApproved == False:
                    block_professional.isApproved = True
                    db.session.commit()
                else:
                    block_professional.isApproved = False
                    db.session.commit()
                return redirect(url_for('admin'))
            except:
                return redirect(url_for('admin'))
        except:
            return redirect(url_for('admin'))

@app.route('/admin/service/<string:s>/<int:i>',methods=["GET","POST"])
@login_required
def admin_add_service(s,i):
    try:
        if request.method=="GET":
            services=Service.query.all()
            return render_template("Admin_Add_Service.html",services=services)
        elif request.method=="POST":
            if s=="a_s":
                service_name = request.form["service_name"]
                service=Service(s_name=service_name)
                db.session.add(service)
                db.session.commit()
                return redirect(url_for(admin))
            elif s=="e_s":
                edited_service_name = request.form["edit_service"]
                service = Service.query.filter_by(s_id=i).first()
                service.s_name=edited_service_name
                db.session.commit()
                print("Deleted")
                return redirect(url_for(admin))
            elif s=="d_s":
                service = Service.query.filter_by(s_id=i).first()
                db.session.delete(service)
                db.session.commit()
                return redirect(url_for(admin))
    except:
        return redirect(url_for('admin_add_service',s='s',i=0))

#User Profile
@app.route('/user/profile/<int:i>/<string:s>',methods=["GET","POST"])
@login_required
def user_profile(i,s):
    try:
        if s=="city":
            print(s)
            city=request.form["city"].strip()
            print(city)
            change_city=User.query.filter_by(u_id=i).first()
            change_city.u_city=city
            db.session.commit()
            return redirect(url_for("uprofile"))
        elif s=="address":
            address=request.form["address"]
            print(address)
            change_address=User.query.filter_by(u_id=i).first()
            change_address.u_address=address
            db.session.commit()
            return redirect(url_for("uprofile"))
        elif s=="email_otp":
            otp=request.form["e_otp"]
            print(otp)
            e_verify=User.query.filter_by(u_id=i).first()
            e_verify.e_verification=True
            db.session.commit()
            return redirect(url_for("uprofile"))
        elif s=='user_image':
            if 'file' not in request.files:
                return 'No file part'

            file = request.files['file']

            if file.filename == '':
                return 'No selected file'
            import os
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file_path=file_path.replace('\\','/')
                file.save(file_path)

                # Save the file path to the database
                new_image = User.query.filter_by(u_id=i).first()
                new_image.u_img_profile=file_path
                db.session.commit()

                return redirect(url_for('uprofile'))

            return 'Invalid file type'
        elif s=='change_phoneno':
            phoneno = request.form["phoneno"]
            u_phoneno = User.query.filter_by(u_id=i).first()
            u_phoneno.u_phoneno = phoneno
            db.session.commit()
            return redirect(url_for("uprofile"))
    except:
        return redirect(url_for("uprofile"))

#Professional Profile
@app.route('/professional/profile/<int:i>/<string:s>',methods=["GET","POST"])
@login_required
def professional_profile(i,s):
    try:
        if s=="city":
            print(s)
            city=request.form["city"].strip()
            print(city)
            change_city=Professional.query.filter_by(p_id=i).first()
            change_city.p_city=city
            db.session.commit()
            return redirect(url_for("pprofile"))
        elif s=="address":
            address=request.form["address"]
            print(address)
            change_address=Professional.query.filter_by(p_id=i).first()
            change_address.p_address=address
            db.session.commit()
            return redirect(url_for("pprofile"))
        elif s=="email_otp":
            otp=request.form["e_otp"]
            print(otp)
            e_verify=Professional.query.filter_by(p_id=i).first()
            e_verify.e_verification=True
            db.session.commit()
            return redirect(url_for("pprofile"))
        elif s=='user_image':
            if 'file' not in request.files:
                return 'No file part'

            file = request.files['file']

            if file.filename == '':
                return 'No selected file'
            import os
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file_path=file_path.replace('\\','/')
                file.save(file_path)

                # Save the file path to the database
                new_image = Professional.query.filter_by(p_id=i).first()
                new_image.p_img_profile=file_path
                db.session.commit()

                return redirect(url_for('pprofile'))

            return 'Invalid file type'
        elif s=='change_phoneno':
            phoneno = request.form["phoneno"]
            p_phoneno = Professional.query.filter_by(p_id=i).first()
            p_phoneno.p_phoneno = phoneno
            db.session.commit()
            return redirect(url_for("pprofile"))
    except:
        return redirect(url_for("pprofile"))

@socketio.on('email_verification')
def email_verification(data):
    email = data['email']
    print(email)
    from random import randint
    otp = randint(1000, 9999)
    send_code = Message(
        subject="Email Verification Code",
        sender="ayushgame2910@gmail.com",
        recipients=[email],
    )
    send_code.body = str(otp)
    mail.send(send_code)
    emit('reponse-otp',{'otp':otp})

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

app.run()