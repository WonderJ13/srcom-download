import argparse
import json
import os
import requests
import sys

API_URI = "https://www.speedrun.com/api/v1/"

def get_json(uri):
    print("GET from {}".format(uri))
    response = requests.get(uri)
    response.raise_for_status()
    return json.loads(response.text)

def get_game_list_from_name(name):
    uri = API_URI + "games?_bulk=1&name=" + name

    json_response = get_json(uri)
    return json_response['data']

def get_int(prompt, max, min=1):
    ret = min-1
    while min > ret or ret >  max:
        num = input(prompt)
        try:
            ret = int(num)
            continue
        except Exception:
            continue
            
    return ret

def pick_game_from_name(name):
    games = get_game_list_from_name(name)
    if len(games) == 0:
        print("Game {} not found".format(name))
        sys.exit(1)
    elif len(games) == 1:
        return games[0]['id']
    else:
        print("{} returned multiple games, pick one:".format(name))

        i = 0
        for game in games:
            i += 1
            print("{}: {}".format(i, game['names']['international']))

        selection = get_int('Select a game: ', i)

        return games[selection-1]['id']

def get_category_ids_from_game_id(game_id):
    uri = API_URI + "games/" + game_id + "/categories?_bulk=1"
    json_response = get_json(uri)

    return json_response['data']

def get_runs_from_category_id(cat_id):
    uri = API_URI + "runs?category=" + cat_id

    runs = []
    while True:
        json_response = get_json(uri)
        runs += json_response['data']

        pagination = json_response['pagination']
        for link in pagination['links']:
            if link['rel'] == "next":
                uri = link['uri']
                break
        else:
            return runs

def generate_game_dict_from_id(game_id):
    categories_json = get_category_ids_from_game_id(game_id)

    game_dict = dict()
    game_dict['game'] = get_json(API_URI + "games/" + game_id)['data']
    game_dict['categories'] = []

    for cat in categories_json:
        category_runs = dict()
        category_runs['category'] = cat
        category_runs['runs'] = get_runs_from_category_id(cat['id'])

        game_dict['categories'].append(category_runs)
    return game_dict

def generate_game_dict_from_game_name(name):
    game_id = pick_game_from_name(name)
    return generate_game_dict_from_id(game_id)

def save_game_dict_to_disk(game_dict):
    game_id = game_dict['game']['id']
    game_id_path = "./games/{}".format(game_id)
    try:
        os.makedirs(game_id_path)
    except Exception:
        pass

    game_file = open("{}/{}".format(game_id_path, "game.json"), 'w')
    game_file.write(json.dumps(game_dict['game']))
    game_file.close()

    for cat in game_dict['categories']:
        cat_id = cat['category']['id']
        cat_id_path = "{}/{}".format(game_id_path, cat_id)
        try:
            os.mkdir(cat_id_path)
        except Exception:
            pass

        cat_file = open("{}/{}".format(cat_id_path, "category.json"), 'w')
        cat_file.write(json.dumps(cat))
        cat_file.close()

        for run in cat['runs']:
            run_id = run['id']
            run_file = open("{}/{}.json".format(cat_id_path, run_id), 'w')
            run_file.write(json.dumps(run))
            run_file.close()
def main():
    parser = argparse.ArgumentParser(description="Download game, category, and run data from speedrun.com", epilog="JSON blobs are saved in a new \"games\" subdirectory. Game and Category subfolders are named based on their speedrun.com assigned id, as well as the run files themselves. Game and Category JSON blobs are named \"game.json\" in their game's subfolder and \"category.json\" in their category's subfolder respectively.")
    parser.add_argument("--name", type=str,
                        help="search the game by name (may prompt user if more than 1 game is returned by speedrun.com")
    parser.add_argument("--id", type=str,
                        help="search the game by its id (overrides --name)")
    args = parser.parse_args()

    game_dict = None
    if not args.id:
        if not args.name:
            parser.print_help()
        else:
            game_dict = generate_game_dict_from_game_name(args.name)
    else:
        game_dict = generate_game_dict_from_id(args.id)
    save_game_dict_to_disk(game_dict)

if __name__ == "__main__":
    main()
