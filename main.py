from flask import Flask,render_template,request,redirect,url_for,flash
from models import db,User,Professional,Admin
from flask_login import LoginManager,login_user,login_required,current_user,logout_user
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///app.db"
app.config["SECRET_KEY"]="#bfkfabwksj%1212"
db.init_app(app)


#Login
login_manager = LoginManager()
login_manager.init_app(app)
# login_manager.login_view='login'

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
    logout_user()
    flash("Logged out!")
    return redirect(url_for("user_login"))

@app.route("/plogout")
@login_required
def p_logout():
    logout_user()
    flash("Logged out!")
    return redirect(url_for("professional_login"))
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
    return render_template("U_Profile.html",email=current_user.u_email)

@app.route('/pprofile')
@login_required
def pprofile():
    return render_template("P_Profile.html",email=current_user.p_email)


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
app.run()