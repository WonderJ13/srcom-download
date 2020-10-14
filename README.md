# srcom-download
srcom-download downloads all game, category, and run data from [https://www.speedrun.com](https://www.speedrun.com) for any given game.

## Requirements
srcom-download uses the python3 library `requests`, this can be downloaded with `pip3 install -r requirements.txt`.

## Examples
`python3 main.py --name 140`

This will prompt the user to pick a specific game, and download all game/category/run data for the selected game to the `./games/` directory.

`python3 main.py --id 9d3r70dl`

This will download all game/category/run data for the game 140 to the `./games/` directory.

## /games/ layout
The layout of the `./games/` folder is structed as such.

`./games/{game_id}/{category_id}/{run_id}.json` such that game_id, category_id, and run_id are ids assigned to them by [https://www.speedrun.com](https://www.speedrun.com).

JSON for the specific game is saved in `./games/{game_id}/game.json`, and JSON for the specific category is saved in `./games/{game_id}/{category_id}/category.json`.