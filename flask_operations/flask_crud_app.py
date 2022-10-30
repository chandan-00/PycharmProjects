from flask import Flask, render_template, request, redirect, url_for
from models import db, EmployeeModel
import logging

app = Flask(__name__)
logging.basicConfig(filename="flask_crud.log", format='%(asctime)s - %(levelname)s - %(message)s', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()
    logger.info('Created a table')


@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        update_id = request.form['update_id']
        delete_id = request.form['delete_id']
        if employee_id == '' and update_id == '' and delete_id == '':
            logger.error('Not entered any values')
            return 'Please enter any value'
        if employee_id == '' and update_id == '' and delete_id != '':
            return redirect(url_for("delete", id=delete_id))
        if employee_id == '' and update_id != '' and delete_id == '':
            return redirect(url_for("update", id=update_id))
        if employee_id != '' and update_id == '' and delete_id == '':
            return redirect(url_for("RetrieveEmployee", id=employee_id))
        else:
            logger.error('Entered more than one value at a time')
            return 'Enter one value at a time'
    logger.info('Back to the homepage')
    return render_template('hello.html')


@app.route('/data/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        name = request.form['name']
        age = request.form['age']
        position = request.form['position']
        employee = EmployeeModel(employee_id=employee_id, name=name, age=age, position=position)
        if employee.employee_id == '' or employee.name == '' or employee.age == '' or employee.position == '':
            logger.error('All details not entered')
            return 'Please enter all details'
        db.session.add(employee)
        db.session.commit()
        logger.info('Added details of an employee to the database')
        return redirect('/data')
    logger.info('Opening create page')
    return render_template('createpage.html')


@app.route('/data')
def RetrieveList():
    employees = EmployeeModel.query.all()
    logger.info('Name and employee id are being displayed')
    return render_template('datalist.html', employees=employees)


@app.route('/data/<int:id>')
def RetrieveEmployee(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if employee:
        logger.info(f'Displaying employee {id}\'s details')
        return render_template('data.html', employee=employee)
    logger.error(f'Employee with id = {id} Doesn\'t exist ')
    return f"Employee with id = {id} Doesn't exist"


@app.route('/data/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if request.method == 'POST':
        if employee:
            db.session.delete(employee)
            db.session.commit()
            name = request.form['name']
            age = request.form['age']
            position = request.form['position']
            employee = EmployeeModel(employee_id=id, name=name, age=age, position=position)
            if employee.employee_id == '' or employee.name == '' or employee.age == '' or employee.position == '':
                logger.error('All details not entered')
                return 'Please enter all details'
            db.session.add(employee)
            db.session.commit()
            logger.warning(f'Updated employee {id}\'s details')
            return redirect(f'/data/{id}')
        logger.error('Wrong employee id entered')
        return f"Employee with id = {id} Does not exist"
    logger.info('Opening update page')
    return render_template('update.html', employee=employee)


@app.route('/data/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if request.method == 'POST':
        if employee:
            db.session.delete(employee)
            db.session.commit()
            logger.warning(f'Deleted employee {id}\'s details')
            return redirect('/data')
        logger.error('Wrong employee id entered')
        return f"Employee with id = {id} Does not exist"
    logger.info('Opening delete page')
    return render_template('delete.html')


@app.route('/data/list', methods=['GET', 'POST'])
def emp_list():
    employees = EmployeeModel.query.all()
    logger.info('Displaying details of all employees')
    return render_template('details.html', employees=employees)


app.run(host='localhost', port=7000, debug=True)
