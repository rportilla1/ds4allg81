import dash
from dash.dependencies import Input, Output, State
from datetime import date
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import pandas as pd
import dash_table
import plotly.express as px
from sqlalchemy import create_engine
import psycopg2 as ps

#### DB Connection
#host = 'ds4apostgresql.cal0piqnh7zy.us-east-2.rds.amazonaws.com'
#port = 5432
#user = 'postgres'
#password = 'ppM0USAxPnPMhwuqQkaW'
#database = 'AMVA'

host = '157.230.55.87'
port = 5432
user = 'postgres'
database = 'AMVA'

try:
    #conn = ps.connect(host=host,database=database,user=user,password=password,port=port)
    conn = ps.connect(host=host,database=database,user=user,port=port)
except ps.OperationalError as e:
    raise e
else:
    print('Connected!')

SQL_Query = pd.read_sql('SELECT * FROM eventosmodelo LIMIT 100', conn)
scatter = px.scatter(SQL_Query, x='longitud', y='latitud')

#### application
app = dash.Dash(__name__)

#### layout
app.layout = html.Div(children=[


#### prueba contenido andres
        html.Div(
            className="banner",
            children=[
                # Change App Name here
                html.Div(
                    className="container scalable",
                    children=[
                        # Change App Name here
                        html.H2(
                            id="banner-title",
                            children=[
                                html.A(
                                    "PUBLIC TRANSPORTATION SYSTEM PLANNING TEAM81",
                                     style={
                                        "text-decoration": "none",
                                        "color": "inherit",
                                    },
                                )
                            ],
                        ),
                        html.A(
                            id="banner-logo",
                            children=[
                                html.Img(src=app.get_asset_url("logo5.png"))
                            ],
                         ),
                    ],
                )
            ],
        ),
        
                           # Row 3 PRUEBA 
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5("INTRODUCCIÓN"),
                                    html.Br([]),
                                    html.P(
                                        "\
                                    El transporte público es un servicio vital para una ciudad, ya que permite a sus ciudadanos desplazarse,                                     viajar y desarrollar la economía de la ciudad. Además, se ha trabajado mucho en el diseño de un sistema                                     de transporte inclusivo, eficiente y sostenible. Sin embargo, ha habido una falta de coordinación de las                                     diferentes partes interesadas y hay una falta de datos confiables para los tomadores de decisiones. Las                                     partes interesadas del sistema de transporte pueden incluir: gobierno, autoridades de tránsito, empresas                                     propietarias de autobuses, formuladores de políticas, fabricantes de autobuses, conductores, usuarios,                                       etc. Pueden tener diferentes intereses y percepciones sobre cómo debería ser un sistema de transporte                                       público y una metodología sistemática para la evaluación de los principales factores de servicio no está                                     disponible, más aún cuando los datos están disponibles, pero son diversos, dispersos y no confiables. El                                     Centro de Operaciones de Transporte Público (GTPC) reconoce que hasta el 40% de los datos capturados                                         para el sistema operativo diario tienen problemas de calidad. Los datos de baja calidad no son adecuados                                     para alimentar el sistema operativo ni utilizarse para el modelado de predicciones, la planificación de                                     rutas óptimas o para la toma de decisiones.",
                                        style={"color": "#ffffff"},
                                        className="row",
                                    ),
                                ],
                                className="product",
                            )
                        ],
                        className="row",
                    ), 
#### prueba contenido andres
    
html.Br([]),
html.H5("EXPLORACIÓN DE DATOS"),
html.Br([]),
    
    
    
dcc.DatePickerRange(id='date_picker', min_date_allowed=date(2019,11,1),
                    max_date_allowed=date(2019,11,30),initial_visible_month =date(2019,11,1),
                    minimum_nights = 0),
dcc.Input(id='input_hour',type='text', placeholder='Start hour', debounce=True,
          pattern= u'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$'),
dcc.Input(id='output_hour',type='text', placeholder='End hour', debounce=True,
          pattern= u'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$'),
html.Button(id= 'date_button', n_clicks=0, children = 'Process'),
    
html.Br([]),
html.H5("ESQUEMA DE RUTAS"),   
    

dcc.Graph(figure=scatter, id='scatter'),
    
html.Br([]),
html.H5("RUTAS REPORTADAS"),      

dash_table.DataTable(id='table',
                     columns =[{'name':i, 'id':i} for i in SQL_Query.columns],
                     data=SQL_Query.head(5).to_dict('records')),
    
html.Br([]),
html.H5("MAPEO"),     
    
html.Div(id='output_date')
], id='layout')

  

#### Interactividad
### Get dates for SQL_query
@app.callback(Output('output_date','children'),
             [Input('date_button', 'n_clicks')],
             [State('date_picker', 'start_date'), State('date_picker','end_date'),
              State('input_hour','value'), State('output_hour','value')])

def date_output(n_clicks,start_date, end_date,in_hour, end_hour):
        return u'''
                The date is "{}" and "{}" and hour "{}" and "{}"'''.format(start_date, end_date,in_hour,end_hour)



#### Initiate server where app will work
if __name__ == '__main__':
    app.run_server(host ='127.0.0.1', debug=True)
