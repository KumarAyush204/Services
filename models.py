from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db=SQLAlchemy()

class User(UserMixin,db.Model):
    __tablename__="user"
    u_id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    u_f_name=db.Column(db.String,nullable=False,unique=True)
    u_l_name = db.Column(db.String, nullable=False, unique=True)
    date_registred=db.Column(db.DateTime,default=db.func.current_timestamp())
    u_city=db.Column(db.String)
    u_address=db.Column(db.String)
    u_phoneno=db.Column(db.Integer,unique=True,nullable=False)
    u_email=db.Column(db.String,unique=True,nullable=False)
    u_pwd=db.Column(db.String,nullable=False)
    u_img_profile=db.Column(db.String)
    isBlock = db.Column(db.Boolean, default=False)
    e_verification = db.Column(db.Boolean, default=False)
    p_verification = db.Column(db.Boolean, default=False)
    # otp=db.Column(db.Integer)

    def get_id(self):
        return f"user-{self.u_id}"

class Professional(UserMixin,db.Model):
    __tablename__="professional"
    p_id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    p_f_name=db.Column(db.String,nullable=False,unique=True)
    p_l_name = db.Column(db.String, nullable=False, unique=True)
    p_date_registred=db.Column(db.DateTime,default=db.func.current_timestamp())
    p_city=db.Column(db.String)
    p_address=db.Column(db.String)
    p_phoneno=db.Column(db.Integer,unique=True,nullable=False)
    p_email=db.Column(db.String,unique=True,nullable=False)
    p_pwd=db.Column(db.String,nullable=False)
    p_img_profile=db.Column(db.String)
    isBlock = db.Column(db.Boolean, default=False)
    isApproved=db.Column(db.Boolean,default=False)
    e_verification = db.Column(db.Boolean, default=False)
    p_verification = db.Column(db.Boolean, default=False)
    s_id = db.Column(db.Integer, db.ForeignKey("service.s_id"))

    def get_id(self):
        return f"prof-{self.p_id}"

class Admin(UserMixin,db.Model):
    __tablename__="admin"
    a_id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    a_email = db.Column(db.String, unique=True, nullable=False)
    a_pwd = db.Column(db.String, nullable=False)

    def get_id(self):
        return f"admin-{self.a_id}"

class Service(UserMixin,db.Model):
    __tablename__="service"
    s_id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    s_name=db.Column(db.String,nullable=False)

class Service_Status(UserMixin,db.Model):
    __tablename__="service_status"
    ss_id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    ss_name=db.Column(db.String,nullable=False)

class Service_Request(UserMixin,db.Model):
    __tablename__ = "service_request"
    sr_id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    u_id=db.Column(db.Integer,db.ForeignKey("user.u_id"))
    p_id=db.Column(db.Integer,db.ForeignKey("professional.p_id"))
    s_id=db.Column(db.Integer,db.ForeignKey("service.s_id"))
    ss_id=db.Column(db.Integer,db.ForeignKey("service_status.ss_id"),default=0)
    time_created=db.Column(db.DateTime,default=db.func.current_timestamp())
    time_finished=db.Column(db.DateTime,nullable=True)