import pandas as pd
from pandas.io.formats import style
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State, MATCH
import plotly.graph_objects as go
from plotly.subplots import make_subplots

app = dash.Dash(__name__, suppress_callback_exceptions=True)

server = app.server

app.title = 'Malaysia Covid-19 Interactive Dashboard'

#Overwrite your CSS setting by including style locally
colors = {
    'background': '#2D2D2D',
    'text': '#E1E2E5',
    'figure_text': '#ffffff',
    'confirmed_text':'#3CA4FF',
    'deaths_text':'#f44336',
    'recovered_text':'#5A9E6F',
    'highest_case_bg':'#393939',
}

#Creating custom style for local use
divBorderStyle = {
    'backgroundColor' : '#393939',
    'borderRadius': '12px',
    'lineHeight': 0.9,
    'height': '150px'
}

#Creating custom style for local use
boxBorderStyle = {
    'borderColor' : '#393939',
    'borderStyle': 'solid',
    'borderRadius': '10px',
    'borderWidth':2,
}

df_malaysia_cases = pd.read_csv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/cases_malaysia.csv')
# print(df_malaysia.head())
df_malaysia_deaths = pd.read_csv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/deaths_malaysia.csv')
# print(df_malaysia_deaths.head())
df_state_cases = pd.read_csv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/cases_state.csv')
# print(df_state_cases.head())
df_state_deaths = pd.read_csv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/deaths_state.csv')
# print(df_state_deaths.head())
df_vax_malaysia = pd.read_csv('https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/vaccination/vax_malaysia.csv')
# print(df_vax_malaysia.head())
df_vax_state =pd.read_csv('https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/vaccination/vax_state.csv')
# print(df_vax_state.head())
df_malaysia_population = pd.read_csv('https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/static/population.csv')
# print(df_malaysia_population.head())


#get states
state_list = df_state_cases['state'].value_counts().index

#data pre-processing
## malaysia cases
malaysia_cases = df_malaysia_cases.copy()
malaysia_deaths = df_malaysia_deaths.copy()
malaysia_cases = malaysia_cases[['date','cases_new','cases_import','cases_recovered']]
malaysia_total_cases = malaysia_cases['cases_new'].sum()
malaysia_total_recovered = malaysia_cases['cases_recovered'].sum()
malaysia_active = malaysia_total_cases - malaysia_total_recovered
past_24hr_increase = malaysia_cases.iloc[-1]['cases_new']
past_24hr_recovery = malaysia_cases.iloc[-1]['cases_recovered']
malaysia_total_deaths = malaysia_deaths['deaths_new'].sum()
past_24hr_deaths = malaysia_deaths.iloc[-1]['deaths_new']

## vaccine data
vax_malaysia = df_vax_malaysia.copy()
vax_state = df_vax_state.copy()
vax_malaysia['Pfizer'] = vax_malaysia['pfizer1'] + vax_malaysia['pfizer2']
vax_malaysia['Sinovac'] = vax_malaysia['sinovac1'] + vax_malaysia['sinovac2']
vax_malaysia['Astra'] = vax_malaysia['astra1'] + vax_malaysia['astra2']
vax_state['Pfizer'] = vax_state['pfizer1'] + vax_state['pfizer2']
vax_state['Sinovac'] = vax_state['sinovac1'] + vax_state['sinovac2']
vax_state['Astra'] = vax_state['astra1'] + vax_state['astra2']
# print(vax_malaysia[['cumul_partial','cumul_full','cumul']])
vax_total = vax_malaysia[['date','cumul_partial','cumul_full']]
vax_daily = vax_malaysia[['date','daily_partial','daily_full']]
# print(vax_total)
# print(vax_daily)
vax_type = vax_malaysia.iloc[:,7:14]
# print(vax_type.iloc[-1])
df_dos1 = vax_malaysia[['pfizer1','sinovac1','astra1','cansino']]
df_dos2 = vax_malaysia[['pfizer2','sinovac2','astra2']]
# print(df_dos1)
# full_vaccinated = vax_malaysia['cumul_full'].iloc[-1]
# partial_vaccinated = vax_malaysia['cumul_partial'].iloc[-1]
# print(full_vaccinated)
df_dos1_state = vax_state[['state','pfizer1','sinovac1','astra1','cansino']]
df_dos2_state = vax_state[['state','pfizer2','sinovac2','astra2']]
# print(df_dos2_state.loc[df_dos2_state['state']=='Kedah'])
# print(df_dos2_state)

## population data
# malaysia_population = df_malaysia_population.copy()
# malaysia__total_population = malaysia_population.iloc[0]['pop']
# print(malaysia__total_population)

## population and vaccination df
# data = {
#     'Total Population':[malaysia__total_population], 
#     'Fully Vaccinated':[full_vaccinated],
#     'Partial Vaccinated':[partial_vaccinated]
# }
# df_vaccination = pd.DataFrame(data=data)
# print(df_vaccination)


##update covid cases graphs 
def get_cases(cases,deaths):
    fig1 = make_subplots(specs=[[{"secondary_y": False}]])
    fig1.add_trace(
        go.Scatter(x=cases['date'], 
        y=cases['cases_new'],
        name='New Cases',
        line=dict(color='#3372FF', width=2),
        # mode='lines+markers',
        fill='tozeroy',)
    ),
    fig1.add_trace(
        go.Scatter(
            x=cases['date'], 
            y=cases['cases_recovered'],
            name='Recovered',
            line=dict(color='#33FF51', width=2),
            # mode='lines+markers',
            fill='tozeroy',
        ),
    ),
    fig1.update_layout(
        title='Cases',
        hovermode='x',
        font=dict(
            family="Courier New, monospace",
            size=14,
            color=colors['figure_text'],
        ),
        legend=dict(
            x=0.02,
            y=1,
            traceorder="normal",
            font=dict(
                family="sans-serif",
                size=12,
                color=colors['figure_text']
            ),
            bgcolor=colors['background'],
            borderwidth=5
        ),
        paper_bgcolor=colors['background'],
        plot_bgcolor=colors['background'],
        margin=dict(l=25, 
                    r=25, 
                    t=25, 
                    b=25
                    ),
        height=400,
    ),

    fig2 = go.Figure(data=go.Scatter(x=deaths['date'], 
            y=deaths['deaths_new'],
            name='Deaths',
            line=dict(color='#FF3333', width=2),
            fill='tozeroy',))

    fig2.update_layout(
        title='Deaths',
        hovermode='x',
        font=dict(
            family="Courier New, monospace",
            size=14,
            color=colors['figure_text'],
        ),
        legend=dict(
            x=0.02,
            y=1,
            traceorder="normal",
            font=dict(
                family="sans-serif",
                size=12,
                color=colors['figure_text']
            ),
            bgcolor=colors['background'],
            borderwidth=5
        ),
        paper_bgcolor=colors['background'],
        plot_bgcolor=colors['background'],
        margin=dict(l=25, 
                    r=25, 
                    t=25, 
                    b=25
                    ),
        height=400,
    ),

    return fig1, fig2

##update covid vaccine graphs
def get_vaccines(dos1,dos2):
    data = [
        go.Pie(
            labels=dos1.columns, 
            values=dos1.sum(),
            domain={'x':[0,1], 'y':[0,1]},
            hole=0.75,
            direction='counterclockwise',
            text = df_dos1.columns,
            # textposition='outside',
            sort=False,
            hovertemplate = "%{label}: %{value} (%{percent})",
            name=''
        ),
        go.Pie(
            labels=dos2.columns, 
            values=dos2.sum(),
            domain={'x':[0.3,0.7], 'y':[0.15,0.85]},
            hole=0.6,
            direction='counterclockwise',
            text=df_dos2.columns,
            textposition='inside',
            sort=False,
            hovertemplate = "%{label}: %{value} (%{percent})",
            name=''
        )
    ]
    fig1=go.Figure(data=data)
    fig1.update_layout(
        font=dict(
            family="Courier New, monospace",
            size=14,
            color=colors['figure_text'],
        ),
        paper_bgcolor=colors['background'],
        plot_bgcolor=colors['background'],
        margin=dict(l=50, 
                    r=50, 
                    t=50, 
                    b=50
                    ),
        # height=400,
    ),
    return fig1

def get_daily_doses(vax_data):
    fig = make_subplots(specs=[[{"secondary_y": False}]])
    fig.add_trace(
        go.Scatter(x=vax_data['date'], 
        y=vax_data['Pfizer'],
        name='Pfizer',
        line=dict(color='#3372FF', width=2),
        # mode='lines+markers',
        fill='tozeroy',)
    ),
    fig.add_trace(
        go.Scatter(
            x=vax_data['date'], 
            y=vax_data['Sinovac'],
            name='Sinovac',
            line=dict(color='#33FF51', width=2),
            # mode='lines+markers',
            fill='tozeroy',
        ),
    ),
    fig.add_trace(
        go.Scatter(
            x=vax_data['date'], 
            y=vax_data['Astra'],
            name='Astra',
            line=dict(color='#FF3333', width=2),
            # mode='lines+markers',
            fill='tozeroy',
        ),
    ),
    fig.add_trace(
        go.Scatter(
            x=vax_data['date'], 
            y=vax_data['cansino'],
            name='Cansino',
            line=dict(color='#B434EB', width=2),
            # mode='lines+markers',
            fill='tozeroy',
        ),
    ),
    fig.update_layout(
        title='Daily Doses',
        hovermode='x',
        font=dict(
            family="Courier New, monospace",
            size=14,
            color=colors['figure_text'],
        ),
        legend=dict(
            x=0.02,
            y=1,
            traceorder="normal",
            font=dict(
                family="sans-serif",
                size=12,
                color=colors['figure_text']
            ),
            bgcolor=colors['background'],
            borderwidth=5
        ),
        paper_bgcolor=colors['background'],
        plot_bgcolor=colors['background'],
        margin=dict(l=35, 
                    r=35, 
                    t=35, 
                    b=35
                    ),
        height=400,
    ),
    return fig

#dash layout
app.layout = html.Div([
    html.H1("Malaysia Covid-19 Interactive Dashboard", style={'text-align': 'center'}),
    ## Dropdown menus
    html.Div([
        html.Div([
            dcc.Dropdown(
                id = 'malaysia',
                options=[
                    {'label':'Malaysia','value':'Malaysia'},
                    {'label':'State','value':'State'}
                ],
                value = 'Malaysia',
                clearable=False,
                style={
                    'color': '#212121',
                } 
                
            ),
        ],
        className='six columns',
        ),
        html.Div([
            dcc.Dropdown(
                id = 'state',
                options=[{'label': i, 'value': i} for i in state_list],
                value='Kedah',
                clearable=False,
            ),
        ],
        className='six columns',
        ),
        html.Br()
    ]),

    html.Br(),

    # Top column display of confirmed, death and recovered total numbers
    html.Div([
        html.Div([
            html.H4(children='Total Cases: ',
                    style={
                        'textAlign': 'center',
                        'color': colors['confirmed_text'],
                    }
                    ),
            html.P(children=[],
                    style={
                        'textAlign': 'center',
                        'color': colors['confirmed_text'],
                        'fontSize': 30,
                    },
                    id='total-cases'
            ),
            html.P(children=[],
                    style={
                        'textAlign': 'center',
                        'color': colors['confirmed_text'],
                    },
                    id='past-24hrs-increases'
            ),
        ],
            style=divBorderStyle,
            className='three columns',
        ),
        html.Div([
            html.H4(children='Total Active Cases: ',
                    style={
                        'textAlign': 'center',
                        'color': colors['confirmed_text'],
                    }
                    ),
            html.P(children=[],
                    style={
                        'textAlign': 'center',
                        'color': colors['confirmed_text'],
                        'fontSize': 30,
                    },
                    id='active-cases'
            ),
            html.P(children=[],
                    style={
                        'textAlign': 'center',
                        'color': colors['confirmed_text'],
                    },
                    id='active-rate'
            ),
        ],
            style=divBorderStyle,
            className='three columns',
        ),
        html.Div(
            [
                html.H4(children='Total Deceased: ',
                    style={
                        'textAlign': 'center',
                        'color': colors['deaths_text'],
                    }
                ),
                html.P(
                    children=[],
                    style={
                        'textAlign': 'center',
                        'color': colors['deaths_text'],
                        'fontSize': 30,
                    },
                    id = 'total-deaths'
                ),
                html.P(
                    children=[],
                    style={
                        'textAlign': 'center',
                        'color': colors['deaths_text'],
                    },
                    id = 'deaths-rate'
                ),
                html.P(
                    children=[],
                    style={
                        'textAlign': 'center',
                        'color': colors['deaths_text'],
                    },
                    id = 'past-24hrs-deaths'
                ),
            ],
            style=divBorderStyle,
            className='three columns'
        ),
        html.Div(
            [
                html.H4(children='Total Recovered: ',
                    style={
                        'textAlign': 'center',
                        'color': colors['recovered_text'],
                    }
                ),
                html.P(children=[],
                    style={
                        'textAlign': 'center',
                        'color': colors['recovered_text'],
                        'fontSize': 30,
                    },
                    id='total-recovered'
                ),
                html.P(children=[],
                    style={
                        'textAlign': 'center',
                        'color': colors['recovered_text'],
                    },
                    id='recovery-rate'
                ),
                html.P(children=[],
                    style={
                        'textAlign': 'center',
                        'color': colors['recovered_text'],
                    },
                    id='past-24hrs-recovery'
                ),
                
            ],
            style=divBorderStyle,
            className='three columns'
        ),
    ], className='row'),

    html.H4(
        children='Covid-19 cases',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'backgroundColor': colors['background'],
        },
        # className='twelve columns'
    ),

    html.Br(),

    ## covid cases graphs
    html.Div([
        html.Div([
            html.Div(
                [
                    dcc.Graph(  
                        id='covid-cases',
                        figure={}
                    ),
                ],
                className='six columns'
            ),
            html.Div(
                [
                    dcc.Graph(
                        id='covid-deaths',
                        figure={}
                    ),
                ],
                className='six columns'
            ),
        ])
    ]),

    ## vaccine graphs
    html.Div([
        html.H4(
            children='Covid-19 Vaccine Progress',
            style={
                'textAlign': 'center',
                'color': colors['text'],
                'backgroundColor': colors['background'],
            },
            className='twelve columns'
        ),
        html.Div([
            html.Div([
                dcc.Graph(
                id='vaccine-type-pie',
            ),
            ], className='columns'),
        ],
            style=boxBorderStyle,
            className='row'
        ),
        html.Br(),
        html.Div([
            html.Div([
                dcc.Graph(
                    id='vaccine-line'
                )
            ],
                className='twelve columns',
                style=boxBorderStyle
            )
        ],
        )
    ])
],
    className='ten columns offset-by-one',
)

@app.callback(
   Output(component_id='state', component_property='style'),
   [Input(component_id='malaysia', component_property='value')])
def show_hide_element(value):
    if value == 'State':
        return {'display':'block', 'color': '#212121'}
    if value == 'Malaysia':
        return {'display': 'none'}

@app.callback(
    [Output('total-cases','children'),
    Output('past-24hrs-increases','children'),
    Output('active-cases','children'),
    Output('active-rate','children'),
    Output('total-deaths','children'),
    Output('deaths-rate','children'),
    Output('past-24hrs-deaths','children'),
    Output('total-recovered','children'),
    Output('recovery-rate','children'),
    Output('past-24hrs-recovery','children')],
    [Input('malaysia','value'),
    Input('state','value')],

)
def get_big_number(slctd_option1,slctd_option2):
    if slctd_option1 == 'Malaysia':
        return [f"{malaysia_total_cases:,d}"],['Past 24hrs increase: +' + f"{past_24hr_increase:,d}"], [f"{malaysia_active:,d}"], \
        ['Active Rate: ' + str(round( malaysia_active/malaysia_total_cases * 100,2))+'%'],[f"{malaysia_total_deaths:,d}"], \
        ['Mortality Rate: ' + str(round(malaysia_total_deaths/malaysia_total_cases * 100, 2)) + '%'], ['Past 24hrs deaths: +' + f"{past_24hr_deaths:,d}"],\
        [f"{malaysia_total_recovered:,d}"], ['Recovery Rate: ' + str(round(malaysia_total_recovered/malaysia_total_cases * 100, 2)) + '%'],\
        ['Past 24hrs recovery: +' + f"{past_24hr_recovery:,d}"]
    elif slctd_option1 == 'State':
        state_cases = df_state_cases.copy()
        state_cases = state_cases[['date','state','cases_new','cases_import','cases_recovered']]
        state_cases = state_cases.loc[state_cases['state']==slctd_option2]
        state_cases.fillna(0,inplace=True)
        state_total_cases = state_cases['cases_new'].sum()
        state_past_24hr_increases = state_cases['cases_new'].iloc[-1]
        state_total_recovered = int(state_cases['cases_recovered'].sum())
        state_active = state_total_cases - state_total_recovered
        state_past_24hrs_recovery = state_cases.iloc[-1]['cases_recovered']
        
        state_deaths = df_state_deaths.copy()
        state_deaths = state_deaths.loc[state_deaths['state'] == slctd_option2]
        state_past_24hr_deaths = state_deaths.iloc[-1]['deaths_new']
        state_total_deaths = state_deaths['deaths_new'].sum()

        return [f"{state_total_cases:,d}"],['Past 24hrs increase: +' + f"{state_past_24hr_increases:,d}"], [f"{state_active:,d}"], \
        ['Active Rate: ' + str(round( state_active/state_total_cases * 100,2))+'%'],[f"{state_total_deaths:,d}"], \
        ['Mortality Rate: ' + str(round(state_total_deaths/state_total_cases * 100, 2)) + '%'], ['Past 24hrs deaths: +' + f"{state_past_24hr_deaths:,d}"],\
        [f"{state_total_recovered:,d}"], ['Recovery Rate: ' + str(round(state_total_recovered/state_total_cases * 100, 2)) + '%'],\
        ['Past 24hrs recovery: +' + f"{int(state_past_24hrs_recovery):,d}"]

@app.callback(
    [Output('covid-cases','figure'),
    Output('covid-deaths','figure')],
    [Input('malaysia','value'),
    Input('state','value')]
)
def update_graphs(slctd_option1,slctd_option2):
    if slctd_option1 == 'Malaysia':
        figs = get_cases(malaysia_cases,df_malaysia_deaths)
        return figs
    elif slctd_option1 == 'State':
        state_cases = df_state_cases.copy()
        state_cases = state_cases[['date','state','cases_new','cases_import','cases_recovered']]
        state_cases = state_cases.loc[state_cases['state']==slctd_option2]
        state_deaths = df_state_deaths.copy()
        state_deaths = state_deaths.loc[state_deaths['state'] == slctd_option2]
        return get_cases(state_cases,state_deaths)

@app.callback(
    [Output('vaccine-type-pie','figure'),
    Output('vaccine-line','figure')
    ],
    [Input('malaysia','value'),
    Input('state','value')]
)
def get_vaccine_graphs(slctd_option1,slctd_option2):
    if slctd_option1 == 'Malaysia':
        pie = get_vaccines(df_dos1,df_dos2)
        line = get_daily_doses(vax_malaysia)
        return pie, line
    elif slctd_option1 == 'State':
        dos1_state = df_dos1_state.copy()
        dos2_state = df_dos2_state.copy()
        vax_states = vax_state.copy()

        dos1_state = dos1_state.loc[dos1_state['state'] == slctd_option2]
        dos2_state = dos2_state.loc[dos2_state['state'] == slctd_option2]
        vax_states = vax_states.loc[vax_states['state'] == slctd_option2]

        pie = get_vaccines(dos1_state,dos2_state)
        line = get_daily_doses(vax_states)
        return pie,line

if __name__ == '__main__':
    app.run_server(debug=True)