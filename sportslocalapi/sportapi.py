import random

from flask import Blueprint, jsonify

sportapi_bp = Blueprint('sportapi', __name__,
                   url_prefix='/',
                   template_folder='templates',
                   static_folder='static', static_url_path='static/sportapi')

sports = []
sport_list = [
]
sport_list.append({
    "Sport": "Track and Field",
    "Practice": "4-6pm, M-F",
    "Coaches": ["Jacobs","Kuelbs","Ruby","Steven", "Kim"],
    "Email": "nighthawkstrack@gmail.com",
    "Website": "nighthawkstrack.com"
})
sport_list .append({
    "Sport": "Tennis",
    "Practice": "4-6pm, M-T",
    "Coaches": "Cherise",
    "Email": "nighthawkstennis@gmail.com",
})


def _find_next_id():
    return max(sports["id"] for sport in sports) + 1


def _init_sports():
    id = 1
    for sport in sport_list:
        sports.append({"id": id, "sport": sport, "var": 0, "var1": 0})
        id += 1


@sportapi_bp.route('/sport')
def get_sport():
    if len(sports) == 0:
        _init_sports()
    return jsonify(random.choice(sports))


@sportapi_bp.route('/sports')
def get_sports():
    if len(sports) == 0:
        _init_sports()
    return jsonify(sports)


if __name__ == "__main__":
    print(random.choice(sport_list))
