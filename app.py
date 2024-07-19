from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///contact-list.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Contact(db.Model):
    # __tablename__ = "contacts"
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(200),nullable = False)
    email = db.Column(db.String(200),nullable = False)
    phone = db.Column(db.String(200),nullable = False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.id}-{self.name}"

@app.route("/",methods=['GET','POST'])
def index():
    if request.method == "POST":
        contact = Contact(
            name=request.form["name"],
            email=request.form["email"],
            phone=request.form["phone"]
        )
        db.session.add(contact)
        db.session.commit()
    # contact = Contact(name = "sachin",email="sachin@gmail.com",phone="123456789")
    # db.session.add(contact)
    # db.session.commit()
    contacts = db.session.execute(db.select(Contact).order_by(Contact.id)).scalars()
    return render_template("index.html",contacts=contacts)

@app.route("/about")
def about():
    return "<p>About page</p>"

@app.route("/update/<int:id>",methods=['GET','POST'])
def update(id):
    contact = db.get_or_404(Contact, id)
    if request.method == "POST":
        contact.name = request.form["name"]
        contact.email = request.form["email"]
        contact.phone = request.form["phone"]
        db.session.add(contact)
        db.session.commit()
        return redirect("/")
   
    return render_template("update.html",contact = contact)
@app.route("/delete/<int:id>")
def delete(id):
    user = db.get_or_404(Contact, id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)