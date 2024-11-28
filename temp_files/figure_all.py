import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import base64
import io

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("График данных", style={'text-align': 'center'}),  # Центрирование заголовка страницы

    # Загрузка файла
    html.Div([
        html.Label("Загрузите файл:", style={'margin-bottom': '5px'}),
        dcc.Upload(
            id='upload-data',
            children=html.Button('Загрузить файл'),
            multiple=False,
            style={'margin-bottom': '15px'}
        )
    ]),

    # Название графика (центральное расположение)
    html.Div([
        html.Label("Название графика:", style={'margin-bottom': '5px'}),
        dcc.Input(id='chart-title', type='text', value='График', style={'width': '100%'}),
    ], style={'margin-bottom': '15px'}),

    # Тип графика
    html.Div([
        html.Div([
            html.Label("Выберите тип графика:", style={'margin-bottom': '5px'}),
            dcc.Dropdown(
                id='chart-type',
                options=[
                    {'label': 'Точечный график (Scatter)', 'value': 'scatter'},
                    {'label': 'Гистограмма (Histogram)', 'value': 'histogram'}
                ],
                value='scatter',
                style={'width': '100%'}
            )
        ], style={'margin-bottom': '15px'})
    ]),

    # Фильтры
    html.Div([
        html.Label("Фильтровать по колонке:", style={'margin-bottom': '5px'}),
        dcc.Dropdown(id='filter-column', options=[], style={'width': '100%', 'margin-bottom': '15px'}),

        html.Label("Оператор для фильтра:", style={'margin-bottom': '5px'}),
        dcc.Dropdown(id='filter-operator', options=[], style={'width': '100%', 'margin-bottom': '15px'}),

        html.Label("Значение для фильтра:", style={'margin-bottom': '5px'}),
        dcc.Input(id='filter-value', type='text', style={'width': '100%'})
    ], style={'margin-bottom': '15px'}),

    # Оси X и Y
    html.Div([
        html.Div([
            html.Label("Выберите колонку для оси X:", style={'margin-bottom': '5px'}),
            dcc.Dropdown(id='x-column', options=[], style={'width': '100%', 'margin-bottom': '15px'})
        ]),
        html.Div([
            html.Label("Выберите колонку для оси Y (для точечного графика):", style={'margin-bottom': '5px'}),
            dcc.Dropdown(id='y-column', options=[], style={'width': '100%'})
        ])
    ], style={'margin-bottom': '15px'}),

    # Сортировка
    html.Div([
        html.Label("Сортировка по значению на графике:", style={'margin-bottom': '5px'}),
        dcc.Dropdown(
            id='sort-order',
            options=[
                {'label': 'По возрастанию', 'value': 'ascending'},
                {'label': 'По убыванию', 'value': 'descending'}
            ],
            value='ascending',
            style={'width': '100%'}
        )
    ], style={'margin-bottom': '15px'}),

    # График
    dcc.Graph(id='graph'),
])


def parse_contents(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    return pd.read_csv(io.StringIO(decoded.decode('utf-8')))


def get_filter_operators(column, df):
    if pd.api.types.is_numeric_dtype(df[column]):
        return [
            {'label': '==', 'value': '=='},
            {'label': '!=', 'value': '!='},
            {'label': '<', 'value': '<'},
            {'label': '<=', 'value': '<='},
            {'label': '>', 'value': '>'},
            {'label': '>=', 'value': '>='}
        ]
    elif pd.api.types.is_string_dtype(df[column]):
        return [
            {'label': '==', 'value': '=='},
            {'label': '!=', 'value': '!='}
        ]
    else:
        return []


@app.callback(
    Output('filter-column', 'options'),
    Output('x-column', 'options'),
    Output('y-column', 'options'),
    Output('filter-operator', 'options'),
    Output('filter-value', 'value'),
    Output('graph', 'figure'),
    Input('upload-data', 'contents'),
    Input('chart-title', 'value'),
    Input('chart-type', 'value'),
    Input('filter-column', 'value'),
    Input('filter-operator', 'value'),
    Input('filter-value', 'value'),
    Input('x-column', 'value'),
    Input('y-column', 'value'),
    Input('sort-order', 'value')
)
def update_graph(contents, title, chart_type, filter_column, filter_operator, filter_value, x_column, y_column, sort_order):
    if contents is None:
        return [], [], [], [], '', {}

    df = parse_contents(contents)

    # Обновление опций для фильтров и осей
    filter_columns = [{'label': col, 'value': col} for col in df.columns]
    x_columns = [{'label': col, 'value': col} for col in df.columns]
    y_columns = [{'label': col, 'value': col} for col in df.columns]

    filter_operator_options = []
    if filter_column:
        filter_operator_options = get_filter_operators(filter_column, df)

    if filter_column and filter_value and filter_operator:
        if pd.api.types.is_numeric_dtype(df[filter_column]):
            filter_value = float(filter_value)
        if filter_operator == '==':
            df = df[df[filter_column] == filter_value]
        elif filter_operator == '!=':
            df = df[df[filter_column] != filter_value]
        elif filter_operator == '<':
            df = df[df[filter_column] < filter_value]
        elif filter_operator == '<=':
            df = df[df[filter_column] <= filter_value]
        elif filter_operator == '>':
            df = df[df[filter_column] > filter_value]
        elif filter_operator == '>=':
            df = df[df[filter_column] >= filter_value]

    if chart_type == 'scatter' and x_column and y_column:
        fig = px.scatter(df, x=x_column, y=y_column, title=title)
    elif chart_type == 'histogram' and x_column:
        hist = df[x_column].value_counts().reset_index()
        hist.columns = [x_column, 'count']
        hist = hist.sort_values(by='count', ascending=(sort_order == 'ascending'))
        fig = px.bar(hist, x=x_column, y='count', title=title)
    else:
        fig = {}

    return filter_columns, x_columns, y_columns, filter_operator_options, filter_value, fig


if __name__ == '__main__':
    app.run_server(debug=True)
