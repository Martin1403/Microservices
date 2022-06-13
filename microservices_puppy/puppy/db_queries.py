from puppy import db
from puppy.api.models import Puppy, Owner


# NEED TO BE TESTED OUTSIDE PACKAGE
# PuppyMicroservices
# - puppy
# -- api
# -- __init__.py
# - db_queries

# CREATE 2 PUPPIES
rufus = Puppy(name="Rufus")
fido = Puppy(name="Fido")

db.session.add_all([rufus, fido])
db.session.commit()

# RETRIEVE PUPPIES FROM DB
puppies = Puppy.query.all()
print(f"Puppies: {puppies}")

# CREATE OWNER
rufus = Puppy(name="Rufus")
puppy = Puppy.query.filter_by(name="Rufus").first()
john = Owner("John", puppy_id=puppy.id)
db.session.add(john)
db.session.commit()

# QUERY ALL
puppies = Puppy.query.all()
print(f"Puppies: {puppies}")
owners = Owner.query.all()
print(f"Owners: {owners}")


# DELETE ALL
for puppy in puppies:
    db.session.delete(puppy)
db.session.commit()

for owner in owners:
    db.session.delete(owner)
db.session.commit()
