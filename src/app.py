import dash
from dash import html, dcc, Input, Output, State
import pandas as pd

app = dash.Dash(__name__)

positions = ['QB', 'RB', 'WR', 'TE']
seasons = [2018, 2019, 2020, 2021, 2022, 2023, 2024]

def get_players_by_position(position):
    players_dict = {
        'QB': ['Patrick Mahomes', 'Josh Allen'],
        'RB': ['Christian McCaffrey', 'Derrick Henry'],
        'WR': ['Justin Jefferson', 'Tyreek Hill'],
        'TE': ['Travis Kelce', 'Mark Andrews']
    }
    return players_dict.get(position, [])

app.layout = html.Div([
    html.H1("NFL Pizza Chart App"),
    html.P("This will eventually let you compare up to 4 players."),
    dcc.Dropdown(
        id='position-dropdown',
        options=[{'label': pos, 'value': pos} for pos in positions],
        placeholder='Select Position'
    ),
    dcc.Dropdown(
        id='player-dropdown',
        options=[],  # Start empty
        placeholder='Select Player',
        style={'display': 'none'}  # Hide initially
    ),
    dcc.Dropdown(
        id='season-dropdown',
        options=[{'label': str(season), 'value': season} for season in seasons],
        placeholder='Select Season'
    )
])

@app.callback(
    Output('player-dropdown', 'options'),
    Output('player-dropdown', 'style'),
    Input('position-dropdown', 'value')
)
def update_player_dropdown(position):
    if position:
        players = get_players_by_position(position)
        options = [{'label': player, 'value': player} for player in players]
        style = {'display': 'block'}
        return options, style
    return [], {'display': 'none'}

if __name__ == "__main__":
    app.run(debug=True)