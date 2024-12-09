from flask import Flask, render_template, send_from_directory
from .model import PokeClient
app = Flask(__name__)
app.jinja_env.filters['zip'] = zip
poke_client = PokeClient()

@app.route('/')
def index():
    """
    Must show all of the pokemon names as clickable links

    Check the README for more detail.
    """
    
    return render_template('index.html',
                           pokemon_list=poke_client.get_pokemon_list(),poke_ids=poke_client.get_pokemon_ids())

@app.route('/pokemon/<pokemon_name>')
def pokemon_info(pokemon_name):
    """
    Must show all the info for a pokemon identified by name

    Check the README for more detail
    """
    return render_template('pokemon_info.html',
                           pokemon_name=pokemon_name,
                           info=poke_client.get_pokemon_info(pokemon_name))

@app.route('/ability/<ability_name>')
def pokemon_with_ability(ability_name):
    """
    Must show a list of pokemon 

    Check the README for more detail
    """
    return render_template('pokemon_with_ability.html',
                           ability_name=ability_name,
                           pokemon_list=poke_client.get_pokemon_with_ability(ability_name))
