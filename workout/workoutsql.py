from __init__ import db
from workout.workoutmodel import Workouts
import random


# this is method called by frontend, it has been randomized between Alchemy and Native SQL for fun
def workouts_all():
    if random.randint(0, 1) == 0:
        table = workouts_all_alc()
    else:
        table = workouts_all_sql()
    return table


# SQLAlchemy extract all users from database
def workouts_all_alc():
    table = Workouts.query.all()
    json_ready = [peep.read() for peep in table]
    return json_ready


# Native SQL extract all users from database
def workouts_all_sql():
    table = db.session.execute('select * from workouts')
    json_ready = sqlquery_2_list(table)
    return json_ready


# SQLAlchemy extract users from database matching term
def workouts_ilike(term):
    """filter Users table by term into JSON list (ordered by User.name)"""
    term = "%{}%".format(term)  # "ilike" is case insensitive and requires wrapped  %term%
    table = Workouts.query.order_by(Workouts.name).filter((Workouts.name.ilike(term))
                                                        | (Workouts.departingLocation.ilike(term))
                                                        | (Workouts.arrivalLocation.ilike(term))
                                                        | (Workouts.departingTime.ilike(term))
                                                        | (Workouts.arrivalTime.ilike(term)))
    return [peep.read() for peep in table]


# SQLAlchemy extract single user from database matching ID
def workout_by_id(workoutid):
    """finds User in table matching userid """
    return Workouts.query.filter_by(workoutID=workoutid).first()


# SQLAlchemy extract single user from database matching departingLocation
def workout_by_departingLocation(departingLocation):
    """finds User in table matching departingLocation """
    return Workouts.query.filter_by(departingLocation=departingLocation).first()

def workout_by_arrivalLocation(arrivalLocation):
    """finds User in table matching departingLocation """
    return Workouts.query.filter_by(arrivalLocation=arrivalLocation).first()

def workout_by_departingTime(departingTime):
    """finds User in table matching departingLocation """
    return Workouts.query.filter_by(departingTime=departingTime).first()

def workout_by_arrivalTime(arrivalTime):
    """finds User in table matching departingLocation """
    return Workouts.query.filter_by(arrivalTime=arrivalTimev).first()



# ALGORITHM to convert the results of an SQL Query to a JSON ready format in Python
def sqlquery_2_list(rows):
    out_list = []
    keys = rows.keys()  # "Keys" are the columns of the sql query
    for values in rows:  # "Values" are rows within the SQL database
        row_dictionary = {}
        for i in range(len(keys)):  # This loop lines up K, V pairs, same as JSON style
            row_dictionary[keys[i]] = values[i]
        row_dictionary["query"] = "by_sql"  # This is for fun a little watermark
        out_list.append(row_dictionary)  # Finally we have a out_list row
    return out_list


# Test queries
if __name__ == "__main__":
    for i in range(1):
        print(workouts_all())
