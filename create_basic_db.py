from Brain import db
from Brain.models import Customer, Task, Partner, Project, Ball, Weekly

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


### Create some projects
# "Misc-Project for every customers
db.session.add_all([Project(name='Misc', customer_id=1),
                    Project(name='Misc', customer_id=2),
                    Project(name='Misc', customer_id=3),
                    Project(name='Misc', customer_id=4)])
db.session.commit()

# some more projects
db.session.add_all([Project(name='Migrate VMs', opp="0815", customer_id=4),
                    Project(name='Openstack', customer_id=4),
                    Project(name='POC', opp="4711", customer_id=3),
                    Project(name='SABA', customer_id=1)])
db.session.commit()


### Create some Tasks
db.session.add_all([Task(text='Code of Conduct FY20', project_id=8),
                    Task(text='Sizing for POC', project_id=7),
                    Task(text='Research configuration', project_id=6),
                    Task(text='Convert VMs from HyperV to VMware', project_id=5),
                    Task(text='Call Mr. Customer', project_id=6),
                    Task(text='Weekly KW49', project_id=1)])
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
