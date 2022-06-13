from puppy import db


class Puppy(db.Model):
    __tablename__ = "puppies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    # ONE TO ONE (One puppy to one owner)
    owner = db.relationship("Owner", backref='puppy', uselist=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Puppy id:{self.id} name:{self.name} owner: {self.owner}"


class Owner(db.Model):

    __tablename__ = "owners"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    puppy_id = db.Column(db.Integer, db.ForeignKey("puppies.id"))

    def __init__(self, name, puppy_id):
        self.name = name
        self.puppy_id = puppy_id

    def __repr__(self):
        return f"{self.name}"