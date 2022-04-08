from __init__ import login_manager, db
from players.playermodel import Players
from flask_login import current_user, login_user, logout_user


# this is method called by frontend, it has been randomized between Alchemy and Native SQL for fun
def players_all():
    """  May have some problems with sql in deployment
    if random.randint(0, 1) == 0:
        table = players_all_alc()
    else:
        table = players_all_sql()
    return table
    """

    return players_all_alc()


# SQLAlchemy extract all players from database
def players_all_alc():
    table = Players.query.all()
    json_ready = [peep.read() for peep in table]
    return json_ready


# Native SQL extract all players from database
def players_all_sql():
    table = db.session.execute('select * from players')
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


# SQLAlchemy extract players from database matching term
def players_ilike(term):
    """filter Players table by term into JSON list (ordered by User.name)"""
    term = "%{}%".format(term)  # "ilike" is case insensitive and requires wrapped  %term%
    table = Players.query.order_by(Players.name).filter((Players.name.ilike(term)) | (Players.email.ilike(term)))
    return [peep.read() for peep in table]


# SQLAlchemy extract single player from database matching ID
def player_by_id(playerid):
    """finds User in table matching playerid """
    return Players.query.filter_by(playerID=playerid).first()


# SQLAlchemy extract single player from database matching email
def player_by_email(email):
    """finds User in table matching email """
    return Players.query.filter_by(email=email).first()


# check credentials in database
def is_player(email, password):
    # query email and return player record
    player_record = player_by_email(email)
    # if player record found, check if password is correct
    return player_record and Players.is_password_match(player_record, password)


# login player based off of email and password
def login(email, password):
    # sequence of checks
    if current_user.is_authenticated:  # return true if player is currently logged in
        return True
    elif is_player(email, password):  # return true if email and password match
        player_row = player_by_email(email)
        login_user(player_row)  # sets flask login_user
        return True
    else:  # default condition is any failure
        return False


# this function is needed for Flask-Login to work.
@login_manager.user_loader
def player_loader(player_id):
    """Check if player login status on each page protected by @login_required."""
    if player_id is not None:
        return Players.query.get(player_id)
    return None


# Authorise new player requires player_name, email, password
def authorize(name, email, phone, password):
    if is_player(email, password):
        return False
    else:
        auth_player = Players(
            name=name,
            email=email,
            password=password,
            phone=phone  # this should be added to playerauthorize.html
        )
        # encrypt their password and add it to the auth_player object
        auth_player.create()
        return True


# logout player
def logout():
    logout_user()  # removes login state of player from session


# Test some queries from implementations above
if __name__ == "__main__":

    # Look at table
    print("Print all at start")
    for player in players_all():
        print(player)
    print()

    """ Password Lookup Sample Code """
    # Expected success on Email and Password lookup
    name = "Adi Khandelwal"
    email = "adikhandelwal@example.com"
    psw = "123adi"
    print(f"Check is_player with valid email and password {email}, {psw}", is_player(email, psw))

    # Expected failure on Email and Password lookup
    psw1 = "1234puffs"
    print(f"Check is_player with invalid password: {email}, {psw1}", is_player(email, psw1))

    """ Authorization Screen Sample Code"""
    # Expected failure as player exists
    print(f"Check authorize with existing email and password: {name}, {psw}", authorize(name, email, psw))

    # Expected success as player does not exist
    name1 = "Coco Puffs"
    email1 = "puffs@example.com"
    print(f"Check authorize with new email and password: {name1}, {psw1}", authorize(name1, email1, psw1))

    # Look at table
    print()
    print("Print all at end")
    for player in players_all():
        print(player)

    # Clean up data from run, so it can run over and over the same
    player_record = player_by_email(email1)
    player_record.delete()
