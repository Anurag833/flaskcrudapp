
from flask import Flask,render_template, request, redirect # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///employee.db"	

db = SQLAlchemy(app)  
app.app_context().push() 

class Employee(db.Model):						
    sno = db.Column(db.Integer, primary_key = True)			
    name = db.Column(db.String(200), nullable = False)			
    email = db.Column(db.String(500), nullable = False)	

# @app.route("/")
# def home():
    
#     # employee = Employee(name = "Employee Name", email = "Employee Email")
#     # db.session.add(employee)
#     # db.session.commit()
#     # allemployee = Employee.query.all()	
#     # return render_template("index.html",allemployee=allemployee)

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']			
        email = request.form['email']			
        employee = Employee(name = name, email = email)	
        db.session.add(employee)
        db.session.commit()
    allemployee = Employee.query.all()
    return render_template("index.html", allemployee=allemployee)
    
@app.route("/delete/<int:sno>")
def delete(sno):
    employee = Employee.query.filter_by(sno=sno).first()
    db.session.delete(employee)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        name = request.form['name']
        email = request.form['email']
        employee = Employee.query.filter_by(sno=sno).first()
        employee.name = name
        employee.email = email
        db.session.add(employee)
        db.session.commit()
        return redirect("/")

    employee = Employee.query.filter_by(sno=sno).first()
    return render_template("update.html", employee=employee)

@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/display")
def display():
    allemployee = Employee.query.all()
    print(allemployee)
    return "This is page 2"

if __name__ == '__main__':
    app.run(debug=True)