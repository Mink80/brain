from Brain import db
from Brain.models import Customer, Task, Partner, Project

### Print all Tasks
print ("\nTasks:")
all_tasks = Task.query.all()
for task in all_tasks:
    print (task)

### print all Projects
print ("\nProjects:")
all_projects = Project.query.all()
for p in all_projects:
    print (p)

### print all Customers
print ("\nCostumers:")
all_customers = Customer.query.all()
for c in all_customers:
    print (c)
