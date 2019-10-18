from brain import db, Customer, Task, Partner, Ball, Weekly
import datetime

# Creates all the tables. Model -> DB Table
db.create_all()

bmw = Customer(name="BMW")
daimler = Customer(name="Daimler", comment="schwierig")
siemens = Customer(name="Siemens", comment="openstack")

# None
print(daimler.id)
print(bmw.id)

#db.session.add_all([bmw, daimler, siemens])
db.session.add(bmw)
db.session.add(siemens)
db.session.add(daimler)

now = datetime.datetime.now()
never = datetime.datetime.min
task1 = Task(text="this is task1", cdate=now, customer=None, ball=Ball.Any ,duedate=never, parent=0, weekly=Weekly.No)
task2 = Task(text="this is task2")

db.session.add(task1)
db.session.add(task2)

# save into db
db.session.commit()

# show IDs
print(daimler.id)
print(bmw.id)

print (task1)
print (task2)

print ("--")

all_tasks = Task.query.all()
print (all_tasks)

all_customer = Customer.query.all()
