from brain import db, Customer, Task, Partner, Ball, Weekly
import datetime

#customer1 =  (Customer.query.filter_by(id=1))
customers = Customer.query.all()
for c in customers:
    print (c)

#print (customer1.all())

# does not work that way
#task2 = Task.query.filter_by(id=2)
#task2.text = "foobar"
#db.session.add(task2)
#db.session.commit()


# INSERT
#task_new = Task(text="mannomann")
#db.session.add(task_new)
#db.session.commit()


# UPDATE
#task2 = Task.query.get(2)
#task2.text = "kai rules"
#db.session.add(task2)
#db.session.commit()


# DELETE - kein fehler wenn es nicht existiert
#task_del = Task.query.get(1)
#db.session.delete(task_del)
# OR
#db.session.delete(Task.query.get(1))

all_tasks = Task.query.all()
for task in all_tasks:
    print (task)
