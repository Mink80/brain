from brain import db, Customer, Task, Partner, Project, Ball, Weekly

### Creates all the tables. Models -> DB Tables
db.create_all()

### Create some Customers
internal = Customer(name="Internal", comment="For Netapp intenal tasks")
bmw = Customer(name="BMW")
daimler = Customer(name="Daimler", comment="schwierig")
siemens = Customer(name="Siemens", comment="focus account")

db.session.add_all([internal,bmw,daimler,siemens])
db.session.commit()

### Create some Partners
db.session.add_all([Partner(name='Computacenter'),
                    Partner(name='Bechtle'),
                    Partner(name='SVA')])
db.session.commit()

### Create some Tasks
db.session.add_all([Task(text='Task1'),
                    Task(text='Task2 foo'),
                    Task(text='Task3 bar')])
db.session.commit()

### Create some projects
db.session.add_all([Project(name='None'),
                    Project(name='Migrate VMs', opp="0815"),
                    Project(name='Openstack'),
                    Project(name='POC', opp="4711")])
db.session.commit()

### Create some relationships
project1 = Project.query.filter_by(id=1).first()
customer2 = Customer.query.filter_by(id=2).first()
task1 = Task.query.filter_by(id=1).first()
task1.project_id = project1.id
task1.customer_id = customer2.id
db.session.add(task1)
db.session.commit()

task3 = Task.query.filter_by(id=3).first()
task3.project_id = project1.id
db.session.add(task3)
db.session.commit()

partner1 = Partner.query.filter_by(id=1).first()
customer3 = Customer.query.filter_by(id=3).first()
project2 = Project.query.filter_by(id=2).first()
project2.customer_id = customer3.id
project2.partner_id = partner1.id
db.session.add(project2)
db.session.commit()

project3 = Project.query.filter_by(id=3).first()
project3.customer_id = customer3.id
db.session.add(project3)
db.session.commit()


### Print all Tasks
print ("Tasks:")
all_tasks = Task.query.all()
for task in all_tasks:
    print (task)

### print all Projects
print ("Projects:")
all_projects = Project.query.all()
for p in all_projects:
    print (p)

### print all Customers
print ("Costumers:")
all_customers = Customer.query.all()
for c in all_customers:
    print (c)

### print all Tasks of Project1:
print ("All tasks of project1:")
for task in project1.tasks:
    print (task)
