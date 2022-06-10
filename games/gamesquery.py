from __init__ import login_manager, db
from cruddy.model import Matches


# this is method called by frontend, it has been randomized between Alchemy and Native SQL for fun
def games_all():
    """  May have some problems with sql in deployment
    if random.randint(0, 1) == 0:
        table = games_all_alc()
    else:
        table = games_all_sql()
    return table
    """

    return games_all_alc()


# SQLAlchemy extract all games from database
def games_all_alc():
    table = Matches.query.all()
    json_ready = [peep.read() for peep in table]
    return json_ready


# Native SQL extract all games from database
def games_all_sql():
    table = db.session.execute('select * from games')
    json_ready = sqlquery_2_list(table)
    return json_ready


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


# SQLAlchemy extract games from database matching term
# SQLAlchemy extract users from database matching term
def games_ilike(term):
    """filter Users table by term into JSON list (ordered by User.name)"""
    term = "%{}%".format(term)  # "ilike" is case insensitive and requires wrapped  %term%
    table = Matches.query.order_by(Matches.date).filter((Matches.date.ilike(term)) | (Matches.team1.ilike(term)))
    json_ready = [peep.read() for peep in table]
    return json_ready


# SQLAlchemy extract single user from database matching ID
def game_by_id(gameid):
    """finds User in table matching userid """
    return Matches.query.filter_by(gameID=gameid).first()


# SQLAlchemy extract single game from database matching email
def game_by_date(date):
    """finds game in table matching email """
    return Matches.query.filter_by(date=date).first()


def game_by_team1(team1):
    """finds game in table matching gameid """
    return Matches.query.filter_by(team1=team1).first()


def game_by_team2(team2):
    """finds game in table matching gameid """
    return Matches.query.filter_by(team2=team2).first()


def game_by_winner(winner):
    """finds game in table matching gameid """
    return Matches.query.filter_by(winner=winner).first()


# Test some queries from implementations above
if __name__ == "__main__":

    # Look at table
    print("Print all at start")
    for game in games_all():
        print(game)
    print()

    # Look at table
    print()
    print("Print all at end")
    for game in games_all():
        print(game)

    # Clean up data from run, so it can run over and over the sam
