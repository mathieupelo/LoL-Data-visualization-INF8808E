import json
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

import preprocess
import bubble

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
app.title = "Projet | INF8808"

# On pourrait charger les textes et autre a mettre ici???
with open('./assets/data/descriptions.json') as f:
    chart_texts = json.load(f)

# On charge les données
with open('./assets/data/countriesData.json') as data_file:
    data = json.load(data_file)

df_2000 = pd.json_normalize(data, '2000')
df_2015 = pd.json_normalize(data, '2015')

df_2000 = preprocess.round_decimals(df_2000)
df_2015 = preprocess.round_decimals(df_2015)

gdp_range = preprocess.get_range('GDP', df_2000, df_2015)
co2_range = preprocess.get_range('CO2', df_2000, df_2015)

df = preprocess.combine_dfs(df_2000, df_2015)
df = preprocess.sort_dy_by_yr_continent(df)


def create_bubble_chart():
    fig = bubble.get_plot(df, gdp_range, co2_range)
    fig = bubble.update_animation_hover_template(fig)
    fig = bubble.update_animation_menu(fig)
    fig = bubble.update_axes_labels(fig)
    fig = bubble.update_template(fig)
    fig = bubble.update_legend(fig)
    fig.update_layout(height=500)
    return fig

app.layout = dbc.Container(fluid=True, children=[
    dbc.Row([
        # Sidebar
        dbc.Col(width=2, className="bg-dark text-white p-4", children=[
            html.H2("Dashboard", className="mb-4"),
            dbc.Button("Bubble Chart", id="btn-bubble", color="primary", className="mb-2 w-100"),
            dbc.Button("Autre Chart", id="btn-other", color="secondary", className="w-100")
        ]),

        # On met le contenu principal ici 
        dbc.Col(width=10, children=[
            html.Header(className="text-center my-4", children=[
                html.H2("Team 21", className="display-4"),
                html.P("Welcome to our interactive dashboard", className="text-muted")
            ]),

            html.Div(id="chart-section", className="px-4")
        ])
    ])
])

@app.callback(
    Output("chart-section", "children"),
    [Input("btn-bubble", "n_clicks"),
     Input("btn-other", "n_clicks")]
)
def update_content(n1, n2):
    ctx = dash.callback_context
    chart = 'btn-bubble'
    if ctx.triggered:
        chart = ctx.triggered[0]['prop_id'].split('.')[0]

    # On select les boutons du sidebar ici
    if chart == 'btn-other':
        content = chart_texts['other']
    else:
        content = chart_texts['bubble']

    return dbc.Row([
        dbc.Col(width=6, children=[
            html.H4(content['title']),
            html.P(content['description1']),
            html.P(content['description2'])
        ]),
        dbc.Col(width=6, children=[
            dcc.Graph(figure=create_bubble_chart())
        ])
    ])


if __name__ == "__main__":
    app.run_server(debug=True)
