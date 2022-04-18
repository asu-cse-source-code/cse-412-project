import os
from igdb.wrapper import IGDBWrapper
import json
import random
from dotenv import load_dotenv

# Load local env variables
load_dotenv()

wrapper = IGDBWrapper(os.getenv("client_id"), os.getenv("access_token"))


def get_games(file: str, rating: str = "> 80", num_games: str = "25"):
    print(num_games)
    print(rating)
    my_bytes_value = wrapper.api_request(
        "games",
        f"fields name, platforms, rating, summary, genres, involved_companies; where rating {rating}; limit {num_games};",
    )
    my_json = my_bytes_value.decode("utf8").replace("'", '"')

    # Load the JSON to a Python list
    data = json.loads(my_json)
    print(f"\n\nRetrieved {len(data)} / {num_games} games from igdb api")
    print("Converting the games for postgresql db...")
    # Format to fit our postgresql DB
    games = [convert_game(game) for game in data if "involved_companies" in game]
    s = json.dumps(games, indent=4, sort_keys=True)

    # dump it back out as formatted JSON
    with open(file, "w") as outfile:
        outfile.write(s)

    # Print successful response
    print("\n\n")
    print("-" * 40)
    print(f"{len(games)} / {len(data)} games added to file successfully.")
    print("-" * 40)


def convert_game(game: dict):
    if int(game["rating"]) > 80:
        price = 60.00
    elif int(game["rating"]) > 50:
        price = float(random.randint(35, 60))
    else:
        price = float(random.randint(10, 35))

    conv_game = {"Price": price}
    for key, val in game.items():
        if key == "genres":
            conv_game["Genre"] = get_field_name_by_id(field=key, id=val[0])
        elif key == "summary":
            conv_game["Description"] = val
        elif key == "involved_companies":
            conv_game["Studio"] = get_company(id=val[0])
        elif key == "name":
            conv_game["Title"] = val
        elif key == "platforms":
            conv_game["Console"] = [
                get_field_name_by_id(field=key, id=console_id) for console_id in val
            ]

    return conv_game


def get_field_name_by_id(field: str, id: int):
    my_bytes_value = wrapper.api_request(
        f"{field}",
        f"fields name; where id = {id};",
    )
    my_json = my_bytes_value.decode("utf8").replace("'", '"')

    # Load the JSON to a Python list & dump it back out as formatted JSON
    data = json.loads(my_json)
    return data[0]["name"]


def get_company(id: int):
    my_bytes_value = wrapper.api_request(
        "involved_companies",
        f"fields company; where id = {id};",
    )
    my_json = my_bytes_value.decode("utf8").replace("'", '"')

    # Load the JSON to a Python list & dump it back out as formatted JSON
    data = json.loads(my_json)
    try:
        return get_field_name_by_id("companies", data[0]["company"])
    except:
        return None


if __name__ == "__main__":
    num_games = input("How many games should I try to retrieve (default 25): ")
    file_loc = input("Filename to ouput the games: ")
    rating = input("Please give rating for the games ex '> 80', '< 50', '= 90' : ")
    if not num_games:
        if not rating:
            get_games(file=file_loc)
        get_games(file=file_loc, rating=rating)
    elif not rating:
        get_games(num_games=num_games, file=file_loc)
    else:
        get_games(num_games=num_games, file=file_loc, rating=rating)
