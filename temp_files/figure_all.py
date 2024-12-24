import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
import plotly.express as px
import io
import base64

# Инициализация приложения Dash
app = dash.Dash(__name__)

# Глобальная переменная для хранения данных
df = pd.DataFrame()

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

def get_aggregation_functions():
    return [
        {'label': 'Без агрегации', 'value': 'none'},
        {'label': 'Сумма', 'value': 'sum'},
        {'label': 'Максимум', 'value': 'max'},
        {'label': 'Минимум', 'value': 'min'},
        {'label': 'Количество', 'value': 'count'}
    ]

# Макет приложения
app.layout = html.Div([
    html.H1("Конструктор графиков", style={'textAlign': 'center'}),

    html.Label("Загрузите файл (CSV):"),
    dcc.Upload(
        id='upload-data',
        children=html.Button("Загрузить файл"),
        multiple=False,
        style={'margin-bottom': '15px'}
    ),

    html.Label("Выберите тип графика:"),
    dcc.Dropdown(
        id='chart-type',
        options=[
            {'label': 'Точечный график (Scatter)', 'value': 'scatter'},
            {'label': 'Линейный график (Line)', 'value': 'line'},
            {'label': 'Столбчатый график (Bar)', 'value': 'bar'},
            {'label': 'Линейчатый график (Horizontal Bar)', 'value': 'horizontal_bar'},
            {'label': 'Круговая диаграмма (Pie)', 'value': 'pie'},
            {'label': 'Кольцевая диаграмма (Donut)', 'value': 'donut'},
            {'label': 'Ящик с усиками (Box plot)', 'value': 'box'}
        ],
        value='scatter',
        style={'width': '100%', 'margin-bottom': '15px'}
    ),

    html.Label("Выберите колонку для оси X или категорий:"),
    dcc.Dropdown(id='x-column', style={'width': '100%', 'margin-bottom': '15px'}),

    html.Label("Выберите колонку для оси Y или значений:"),
    dcc.Dropdown(id='y-column', style={'width': '100%', 'margin-bottom': '15px'}),

    # Фильтры
    html.Div([
        html.Label("Фильтровать по колонке:", style={'margin-bottom': '5px'}),
        dcc.Dropdown(id='filter-column', options=[], style={'width': '100%', 'margin-bottom': '15px'}),

        html.Label("Оператор для фильтра:", style={'margin-bottom': '5px'}),
        dcc.Dropdown(id='filter-operator', options=[], style={'width': '100%', 'margin-bottom': '15px'}),

        html.Label("Значение для фильтра:", style={'margin-bottom': '5px'}),
        dcc.Input(id='filter-value', type='text', style={'width': '100%'}),
    ], style={'margin-bottom': '15px'}),

    html.Label("Сортировка данных по оси Y:"),
    dcc.Dropdown(
        id='sort-order',
        options=[
            {'label': 'По возрастанию', 'value': 'ascending'},
            {'label': 'По убыванию', 'value': 'descending'}
        ],
        value='descending',
        style={'width': '100%', 'margin-bottom': '15px'}
    ),

    html.Label("Выберите функцию агрегации:"),
    dcc.Dropdown(
        id='aggregation-function',
        options=get_aggregation_functions(),
        value='none',
        style={'width': '100%', 'margin-bottom': '15px'}
    ),

    html.Label("Введите заголовок графика:"),
    dcc.Input(id='chart-title', type='text', value='', style={'width': '100%', 'margin-bottom': '15px'}),

    html.Button("Построить график", id='submit-button', n_clicks=0, style={'margin-bottom': '15px'}),

    dcc.Graph(id='graph-output')
])

# Функция для обработки загруженного файла
@app.callback(
    [Output('x-column', 'options'),
     Output('y-column', 'options'),
     Output('filter-column', 'options')],
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def load_data(contents, filename):
    global df
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            if filename.endswith('.csv'):
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            else:
                return [], [], []
        except Exception as e:
            print(f"Ошибка загрузки файла: {e}")
            return [], [], []
    column_options = [{'label': col, 'value': col} for col in df.columns]
    return column_options, column_options, column_options

@app.callback(
    Output('filter-operator', 'options'),
    Input('filter-column', 'value')
)
def update_filter_operators(column):
    if column and column in df.columns:
        return get_filter_operators(column, df)
    return []

# Построение графика
@app.callback(
    Output('graph-output', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('chart-type', 'value'),
     State('x-column', 'value'),
     State('y-column', 'value'),
     State('filter-column', 'value'),
     State('filter-operator', 'value'),
     State('filter-value', 'value'),
     State('sort-order', 'value'),
     State('aggregation-function', 'value'),
     State('chart-title', 'value')]
)
def update_graph(n_clicks, chart_type, x_column, y_column, filter_column, filter_operator, filter_value, sort_order, aggregation_function, title):
    if df.empty or not x_column or (chart_type not in ['pie', 'donut'] and not y_column):
        return {}

    filtered_df = df.copy()

    # Фильтрация данных
    if filter_column and filter_operator and filter_value:
        try:
            # Явная обработка ошибок преобразования в числовой формат
            filter_value = pd.to_numeric(filter_value, errors='coerce') if pd.to_numeric(filter_value, errors='coerce') else filter_value
            if filter_operator == '==':
                filtered_df = filtered_df[filtered_df[filter_column] == filter_value]
            elif filter_operator == '!=':
                filtered_df = filtered_df[filtered_df[filter_column] != filter_value]
            elif filter_operator == '<':
                filtered_df = filtered_df[filtered_df[filter_column] < float(filter_value)]
            elif filter_operator == '<=':
                filtered_df = filtered_df[filtered_df[filter_column] <= float(filter_value)]
            elif filter_operator == '>':
                filtered_df = filtered_df[filtered_df[filter_column] > float(filter_value)]
            elif filter_operator == '>=':
                filtered_df = filtered_df[filtered_df[filter_column] >= float(filter_value)]
        except Exception as e:
            print(f"Ошибка фильтрации: {e}")

    # Применение агрегации
    if aggregation_function != 'none' and y_column in filtered_df.columns:
        if aggregation_function == 'sum':
            filtered_df = filtered_df.groupby(x_column).sum().reset_index()
        elif aggregation_function == 'max':
            filtered_df = filtered_df.groupby(x_column).max().reset_index()
        elif aggregation_function == 'min':
            filtered_df = filtered_df.groupby(x_column).min().reset_index()
        elif aggregation_function == 'count':
            filtered_df = filtered_df.groupby(x_column).count().reset_index()

    # Сортировка данных по значениям оси Y
    if sort_order == 'ascending' and y_column in filtered_df.columns:
        filtered_df = filtered_df.sort_values(by=y_column, ascending=True)
    elif sort_order == 'descending' and y_column in filtered_df.columns:
        filtered_df = filtered_df.sort_values(by=y_column, ascending=False)

    # Построение графика в зависимости от выбранного типа
    if chart_type == 'scatter':
        fig = px.scatter(filtered_df, x=x_column, y=y_column, title=title)

    elif chart_type == 'line':
        fig = px.line(filtered_df, x=x_column, y=y_column, title=title)

    elif chart_type == 'bar':
        fig = px.bar(filtered_df, x=x_column, y=y_column, title=title)

    elif chart_type == 'horizontal_bar':
        fig = px.bar(filtered_df, x=y_column, y=x_column, title=title, orientation='h')

    elif chart_type == 'pie':
        fig = px.pie(filtered_df, names=x_column, values=y_column, title=title)

    elif chart_type == 'donut':
        fig = px.pie(filtered_df, names=x_column, values=y_column, title=title, hole=0.3)

    elif chart_type == 'box':
        fig = px.box(filtered_df, x=x_column, y=y_column, title=title)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)