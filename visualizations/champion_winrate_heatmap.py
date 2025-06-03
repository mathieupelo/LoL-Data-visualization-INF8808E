import json
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Output, Input

# Constants
data_path = "D:/Poly/Project/data/2025_LoL_esports_match_data_from_OraclesElixir.csv"
img_map_path = './utils/champion_images.json'

# Load champion image mapping
with open(img_map_path, 'r') as f:
    img_map = json.load(f)

# Load data
def load_data(path):
    df = pd.read_csv(path, low_memory=False)
    for col in ['position','champion','result','patch']:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
    df['win'] = df['result'].map({1:1,0:0})
    df['pick'] = 1
    return df

# Compute metrics
def compute_metrics(df, metric, patches, top_n=10):
    metrics = {}
    for p in patches:
        sub = df if p=='All' else df[df['patch']==p]
        total = len(sub)
        # Group and filter champions with at least 3 games
        grp = (
            sub.groupby(['position','champion'])
               .agg(wins=('win','sum'), picks=('pick','sum'))
               .reset_index()
        )
        grp = grp[grp['picks'] >= 5]
        # Compute rates
        grp['win_rate'] = grp['wins'] / grp['picks']
        grp['pick_rate'] = grp['picks'] / total
        # Get top N per role
        top = (
            grp.sort_values(['position', metric], ascending=[True, False])
               .groupby('position')
               .head(top_n)
        )
        roles = sorted(top['position'].unique())
        ranks = [f"Rank {i+1}" for i in range(top_n)]
        z, txt, cd, imgs = [], [], [], []
        for role in roles:
            subr = top[top['position']==role].nlargest(top_n, metric)
            vals = subr[metric].tolist()
            names = subr['champion'].tolist()
            games = subr['picks'].tolist()
            # Pad to ensure consistent matrix size
            while len(vals) < top_n:
                vals.append(None)
                names.append('')
                games.append(None)
            z.append(vals)
            txt.append(names)
            cd.append(games)
            # Map champion names to image URLs
            cell_imgs = [img_map.get(ch) for ch in names]
            imgs.append(cell_imgs)
        metrics[p] = dict(z=z, txt=txt, cd=cd, imgs=imgs, roles=roles, ranks=ranks)
    return metrics

# Initialize
df = load_data(data_path)
patches = ['All'] + sorted(df['patch'].unique())
metrics_map = compute_metrics(df,'win_rate',patches)
pick_map = compute_metrics(df,'pick_rate',patches)

# Dash App
app = Dash(__name__)
app.layout = html.Div(style={'backgroundColor':'#272822','color':'#F8F8F2','fontFamily':'Cinzel, serif'}, children=[
    html.H2("LoL Role Heatmap", style={'textAlign':'center'}),
    html.Div([
        html.Label('Patch:', style={'marginRight':'10px'}),
        dcc.Dropdown(id='patch', options=[{'label':p,'value':p} for p in patches], value='All', clearable=False,
                     style={'width':'200px','display':'inline-block','color':'#000'}),
        html.Div([html.Label('Metric:'),
                  dcc.RadioItems(id='metric', options=[{'label':'Win Rate','value':'win_rate'},{'label':'Pick Rate','value':'pick_rate'}],
                                value='win_rate', inline=True, labelStyle={'marginRight':'10px'})],
                 style={'display':'inline-block','marginLeft':'50px'})
    ]),
    dcc.Graph(id='heatmap', config={'displayModeBar':False})
])

# Callback
@app.callback(
    Output('heatmap','figure'),
    Input('patch','value'),
    Input('metric','value')
)
def update_heatmap(selected_patch, selected_metric):
    data = metrics_map if selected_metric=='win_rate' else pick_map
    m = data[selected_patch]
    fig = go.Figure(go.Heatmap(
        z=m['z'], x=m['ranks'], y=m['roles'], text=m['txt'], customdata=m['cd'],
        hovertemplate='<b>%{y}</b><br>%{x}<br>Champion: %{text}<br>'+('Win Rate' if selected_metric=='win_rate' else 'Pick Rate')+': %{z:.2%}<br>Games: %{customdata:d}<extra></extra>',
        colorscale='Blues' if selected_metric=='win_rate' else 'Purples',
        colorbar=dict(title=('Win Rate' if selected_metric=='win_rate' else 'Pick Rate'), tickformat='.0%'),
        showscale=True
    ))
    # add images
    for i, role in enumerate(m['roles']):
        for j, url in enumerate(m['imgs'][i]):
            if url:
                fig.add_layout_image(dict(source=url, x=j, y=i, xref='x', yref='y', sizex=1, sizey=1,
                                          xanchor='center', yanchor='middle', layer='above', sizing='contain'))
    fig.update_layout(
        template='plotly_dark', plot_bgcolor='#272822', paper_bgcolor='#272822',
        font=dict(size=14),
        title=f"{selected_patch} – {'Win Rate' if selected_metric=='win_rate' else 'Pick Rate'}",
        xaxis_title='Rank', yaxis_title='Role'
    )
    return fig

if __name__=='__main__':
    app.run(debug=True)
