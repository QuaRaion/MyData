from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.db import connection
import pandas as pd
import pyarrow.parquet as pq
from django.contrib.auth.decorators import login_required
from files.models import *
from .models import *
from django_plotly_dash import DjangoDash
from dash import dcc, html, Input, Output, State
import plotly.express as px

@login_required
def render_charts_page (request):
    user_files = File.objects.filter(user=request.user).order_by('-created_time')
    public_files = File.objects.filter(is_public=True).order_by('-name')
    
    return render(request, 'charts/charts_page.html', {'user_files':user_files, 'public_files':public_files})

# class NewChart(DetailView):
#     model = File
#     template_name = 'charts/create_chart_page.html'
#     context_object_name = 'file'

#     def get(self, request, pk):
#         file = get_object_or_404(File, file_id=pk)

#         try:
#             df = pd.read_parquet(file.path.path)
#         except Exception as e:
#             return render(request, 'error', {'message': f'Ошибка чтения файла: {e}'})        
            
#         columns = list(df.columns)

#         return render(request, 'charts/prev_create_chart_page.html', {'columns': columns, 'file_name': file.name})


def render_error_page(request, pk):
    p = pk
    return render(request, 'charts/error_page.html')


def create_chart_page(request, pk):
    file_instance = get_object_or_404(File, file_id=pk)

    try:
        df = pd.read_parquet(file_instance.path.path)
    except Exception as e:
        return render(request, 'charts/error_page.html', {'error': str(e)})

    app = DjangoDash("ChartBuilder")

    # функция для получения операторов фильтрации
    def get_filter_operators(column):
        if pd.api.types.is_numeric_dtype(df[column]):
            return [
                {'label': 'равно', 'value': '=='},
                {'label': 'не равно', 'value': '!='},
                {'label': 'меньше', 'value': '<'},
                {'label': 'меньше или равно', 'value': '<='},
                {'label': 'больше', 'value': '>'},
                {'label': 'больше или равно', 'value': '>='}
            ]
        elif pd.api.types.is_string_dtype(df[column]):
            return [
                {'label': 'равно', 'value': '=='},
                {'label': 'не равно', 'value': '!='}
            ]
        else:
            return []

    # функция для получения функций агрегации
    def get_aggregation_functions():
        return [
            {'label': 'без агрегации', 'value': 'none'},
            {'label': 'сумма', 'value': 'sum'},
            {'label': 'максимум', 'value': 'max'},
            {'label': 'минимум', 'value': 'min'},
            {'label': 'количество', 'value': 'count'}
        ]

    app.layout = html.Div([
        html.Label("Тип графика"),
        dcc.Dropdown(
            id='chart-type',
            options=[
                {'label': 'Точечный график (Scatter)', 'value': 'scatter'},
                {'label': 'Линейный график (Line)', 'value': 'line'},
                {'label': 'Столбчатый график (Bar)', 'value': 'bar'},
                {'label': 'Линейчатый график (Horizontal Bar)', 'value': 'horizontal_bar'},
                {'label': 'Круговая диаграмма (Pie)', 'value': 'pie'},
                {'label': 'Кольцевая диаграмма (Donut)', 'value': 'donut'}
            ],
            value='scatter',
            style={'width': '100%', 'margin-bottom': '15px'}
        ),

        html.Label("Значения для оси X (категорий)"),
        dcc.Dropdown(id='x-column', style={'width': '100%', 'margin-bottom': '15px'}),
        
        html.Label("Значения для оси Y (значений)"),
        dcc.Dropdown(id='y-column', style={'width': '100%', 'margin-bottom': '15px'}),
        html.H3("Фильтры"),
        html.Div([
            html.Div([
                html.Label("Столбец"),
                dcc.Dropdown(id='filter-column', options=[], style={'width': '100%'}),
            ], style={'flex': '1', 'margin-right': '10px'}),  # Каждый блок занимает 1 часть свободного пространства

            html.Div([
                html.Label("Условие"),
                dcc.Dropdown(id='filter-operator', options=[], style={'width': '100%'}),
            ], style={'flex': '1', 'margin-right': '10px'}), 

            html.Div([
                html.Label("Значение"),
                dcc.Input(id='filter-value', type='text', style={'width': '100%'}),
            ], style={'flex': '1'}), 

        ], style={
            'display': 'flex',
            'align-items': 'flex-start',  # Выровнять элементы по верху
            'margin-bottom': '15px'
        }),

        html.Label("Сортировка данных по оси Y"),
        dcc.Dropdown(
            id='sort-order',
            options=[
                {'label': 'по возрастанию', 'value': 'ascending'},
                {'label': 'по убыванию', 'value': 'descending'}
            ],
            value='descending',
            style={'width': '100%', 'margin-bottom': '15px'}
        ),

        html.Label("Агрегация"),
        dcc.Dropdown(
            id='aggregation-function',
            options=get_aggregation_functions(),
            value='none',
            style={'width': '100%', 'margin-bottom': '15px'}
        ),

        html.Label("Заголовок чарта"),
        dcc.Input(id='chart-title', type='text', value='', style={'width': '100%', 'margin-bottom': '15px'}),

        html.Button("Построить график", id='submit-button', n_clicks=0, style={'margin-bottom': '15px'}),
        dcc.Graph(id='graph-output')
    ])

    @app.callback(
        [Output('x-column', 'options'),
         Output('y-column', 'options'),
         Output('filter-column', 'options')],
        Input('x-column', 'value')
    )
    def load_data(_):
        column_options = [{'label': col, 'value': col} for col in df.columns]
        return column_options, column_options, column_options

    @app.callback(
        Output('filter-operator', 'options'),
        Input('filter-column', 'value')
    )
    def update_filter_operators(column):
        if column and column in df.columns:
            return get_filter_operators(column)
        return []

    @app.callback(
        Output('graph-output', 'figure'),
        Input('submit-button', 'n_clicks'),
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

        # фильтрация данных
        if filter_column and filter_operator and filter_value:
            try:
                filter_value = pd.to_numeric(filter_value, errors='coerce') if pd.api.types.is_numeric_dtype(df[filter_column]) else filter_value
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

        # применение агрегации
        if aggregation_function != 'none' and y_column in filtered_df.columns:
            if aggregation_function == 'sum':
                filtered_df = filtered_df.groupby(x_column).sum().reset_index()
            elif aggregation_function == 'max':
                filtered_df = filtered_df.groupby(x_column).max().reset_index()
            elif aggregation_function == 'min':
                filtered_df = filtered_df.groupby(x_column).min().reset_index()
            elif aggregation_function == 'count':
                filtered_df = filtered_df.groupby(x_column).count().reset_index()

        # сортировка данных по значениям оси Y
        if sort_order == 'ascending' and y_column in filtered_df.columns:
            filtered_df = filtered_df.sort_values(by=y_column, ascending=True)
        elif sort_order == 'descending' and y_column in filtered_df.columns:
            filtered_df = filtered_df.sort_values(by=y_column, ascending=False)

        # построение чарта
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

        return fig

    return render(request, 'charts/create_chart_page.html', {'file': file_instance, 'dataframe': df})
