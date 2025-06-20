import pandas as pd
import glob
import plotly.express as px
import dash
from dash import Dash, dcc, html, Input, Output, callback
import os
import numpy as np


def get_consistent_color_map(df):
    """Génère un mapping de couleurs cohérent pour toutes les ligues présentes"""
    all_leagues = set()
    
    # Collecter toutes les ligues possibles dans le dataset
    for position in ['Top', 'Jungle', 'Mid', 'Bot', 'Support']:
        for league_filter in ['all', 'major']:
            temp_df = preprocess(df, position_filter=position, league_filter=league_filter)
            if not temp_df.empty:
                all_leagues.update(temp_df['league'].unique())
    
    # Créer un mapping fixe avec des couleurs Plotly
    colors = px.colors.qualitative.Set1 + px.colors.qualitative.Set2
    league_colors = {}
    for i, league in enumerate(sorted(all_leagues)):
        league_colors[league] = colors[i % len(colors)]
    
    return league_colors


BASE_DIR = os.path.dirname(__file__)                   # …/project_root/charts
DATA_DIR = os.path.join(BASE_DIR, '..', 'assets', 'data')
dataset_path = os.path.abspath(DATA_DIR)               # …/project_root/assets/data

def concat_datasets(path):
    files = glob.glob(os.path.join(dataset_path, '*.csv'))

    all_df = []
    for file in files:
        df = pd.read_csv(file, low_memory=False)
        all_df.append(df)

    concat_df = pd.concat(all_df, ignore_index=True)

    return concat_df


def preprocess(df, position_filter=None, league_filter=None):
    """Préprocesse les données pour le winrate des joueurs"""
    # Supprimer les lignes sans nom de joueur
    df = df[df['playername'].notna()]
    df = df[df['teamname'].notna()]
    df = df[df['league'].notna()]

    # Standardiser les noms de positions
    df['position'] = df['position'].replace({
        'bot': 'Bot',
        'jng': 'Jungle', 
        'mid': 'Mid',
        'sup': 'Support',
        'top': 'Top'
    })
    
    # Filtrer par ligue si spécifié
    if league_filter == 'major':
        df = df[df['league'].isin(['LCK', 'LEC', 'LCS'])]
    elif league_filter in ['LCK', 'LEC', 'LCS']:
        df = df[df['league'] == league_filter]


    # Calculer le winrate par joueur avec toutes les informations
    winrate_df = df.groupby(['league', 'teamname', 'position', 'playername'])['result'].agg(['sum', 'count']).reset_index()
    winrate_df.columns = ['league', 'teamname', 'position', 'playername', 'wins', 'games_played']

    # Pour chaque joueur, sommer tous ses wins et games across toutes ses équipes
    final_stats = winrate_df.groupby(['playername', 'position']).agg({
        'wins': 'sum',           # Somme de tous les wins
        'games_played': 'sum',   # Somme de tous les games
        'teamname': lambda x: ' / '.join(x.unique()),  # Concatener les équipes
        'league': lambda x: ' / '.join(x.unique())     # Concatener les ligues
    }).reset_index()

    # Calculer le winrate global (pondéré automatiquement par le nombre de games)
    final_stats['winrate'] = (final_stats['wins'] / final_stats['games_played'] * 100).round(2)
    
    # Filtrer les joueurs avec au moins 10 matchs AU TOTAL
    min_games=10
    final_stats = final_stats[final_stats['games_played'] >= min_games]
    
    # Filtrer par position si spécifié
    if position_filter and position_filter != 'All':
        final_stats = final_stats[final_stats['position'] == position_filter]
    
    # Trier par winrate décroissant et prendre le top 20
    final_stats = final_stats.sort_values('winrate', ascending=True).tail(10)
    
    return final_stats


def get_plot(df, position_filter):
    # Créer le texte personnalisé pour chaque barre
    df['hover_text'] = df.apply(lambda row: 
        f"{row['playername']}<br>" +
        f"Team: {row['teamname']}<br>" +
        f"League: {row['league']}<br>" +
        f"Winrate: {row['winrate']:.1f}%<br>" +
        f"Games: {row['games_played']}", axis=1)
    
    df['bar_text'] = df['winrate'].astype(str) + '%'
    
    fig = px.bar(
        df,
        x='winrate',
        y='playername',
        orientation='h',
        color='league',
        color_discrete_map=LEAGUE_COLOR_MAP,
        title=f'Top {len(df)} {position_filter} Players by Winrate',
        hover_data={
            'teamname': True,
            'games_played': True,
            'winrate': ':.2f%'
        },
        text='bar_text'
    )
    
    # Inverser l'ordre pour avoir le meilleur en haut
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    
    return fig


def update_axes(fig):
    """Mettre à jour les axes"""
    fig.update_xaxes(title_text='Winrate (%)')
    fig.update_yaxes(title_text='Player Name')
    return fig


def make_figure(position='Mid', league_filter='major'):
    filter_df = preprocess(df, position_filter=position, league_filter=league_filter)

    """Créer la figure avec le style"""
    fig = get_plot(filter_df, position_filter=position)
    fig.update_layout(
        height=800, 
        width=1000, 
        dragmode=False,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        plot_bgcolor="#2c2f3e",
        paper_bgcolor="#2c2f3e",
        legend_title='League',
        font=dict(
            family="Beaufort, sans-serif",
            size=12,
            color="#fff"
        )
    )
    fig = update_axes(fig)
    return fig


def layout():
    """Layout de la page"""
    fig = make_figure()

    return html.Div(className='winrate-players', children=[
        html.Header(children=[
            html.H1('Player Winrates'),
            html.H2('Top Performers by Role')
        ]),
        html.Main(className='viz-container', children=[
            html.Div(
                className='dropdown-menus',
                children=[
                    html.Div([
                        html.Label('Select Role:', style={'color': '#fff', 'margin-bottom': '5px'}),
                        dcc.Dropdown(
                            id='position-dropdown',
                            options=[
                                {'label': 'Top Lane', 'value': 'Top'},
                                {'label': 'Jungle', 'value': 'Jungle'},
                                {'label': 'Mid Lane', 'value': 'Mid'},
                                {'label': 'Bot Lane', 'value': 'Bot'},
                                {'label': 'Support', 'value': 'Support'}
                            ],
                            value='Top',
                            clearable=False,
                            style={'width': '200px'}
                        )
                    ], style={'display': 'inline-block', 'margin-right': '20px'}),
                    
                    html.Div([
                        html.Label('Select League:', style={'color': '#fff', 'margin-bottom': '5px'}),
                        dcc.Dropdown(
                            id='league-dropdown',
                            options=[
                                {'label': 'All Leagues', 'value': 'all'},
                                {'label': 'Major Leagues (LCK, LEC, LCS)', 'value': 'major'},
                                {'label': 'LCK', 'value': 'LCK'},
                                {'label': 'LEC', 'value': 'LEC'},
                                {'label': 'LCS', 'value': 'LCS'}
                            ],
                            value='all',
                            clearable=False,
                            style={'width': '250px'}
                        )
                    ], style={'display': 'inline-block'})
                ],
                style={'margin-bottom': '20px', 'display': 'flex', 'flexDirection': 'column', 'alignItems': 'flex-start'}
            ),
            
            dcc.Graph(
                id='winrate-graph', 
                className='graph', 
                figure=fig, 
                config=dict(
                    scrollZoom=False,
                    showTips=False,
                    showAxisDragHandles=False,
                    doubleClick=False,
                    displayModeBar=False,
                )
            ),
        ])
    ])


@callback(
    Output('winrate-graph', 'figure'),
    Input('position-dropdown', 'value'),
    Input('league-dropdown', 'value')
)
def update_winrate_chart(position_value, league_value):
    """Callback pour mettre à jour le graphique selon le filtre de position"""
    
    # Appliquer le filtre
    filtered_df = preprocess(df, position_filter=position_value, league_filter=league_value)
    
    # Créer le nouveau graphique
    new_fig = get_plot(filtered_df, position_filter=position_value)
    new_fig.update_layout(
        height=800, 
        width=1000, 
        dragmode=False,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        plot_bgcolor="#2c2f3e",
        paper_bgcolor="#2c2f3e",
        legend_title='League',
        font=dict(
            family="Beaufort, sans-serif",
            size=12,
            color="#fff"
        )
    )
    new_fig.update_traces(textposition='outside')
    new_fig = update_axes(new_fig)
    """
    # Créer le résumé des statistiques
    if len(filtered_df) > 0:
        avg_winrate = filtered_df['winrate'].mean()
        total_players = len(filtered_df)
        top_player = filtered_df.iloc[-1]  # Dernier car trié en ascending
        
        stats_text = html.Div([
            html.P(f"📊 Players shown: {total_players}"),
            html.P(f"🏆 Best performer: {top_player['playername']} ({top_player['team']}) - {top_player['winrate']}%"),
        ])
    else:
        stats_text = html.P("No data available for the selected filter.")
    """
    return new_fig#, stats_text


# Charger et préprocesser les données au démarrage
df = concat_datasets(dataset_path)
LEAGUE_COLOR_MAP = get_consistent_color_map(df)
filter_df = preprocess(df)
