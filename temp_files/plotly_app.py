import pandas as pd
import plotly.express as px
import io

def load_parquet(file_path):
    try:
        return pd.read_parquet(file_path)
    except Exception as e:
        print(f"Ошибка загрузки файла: {e}")
        return pd.DataFrame()

df = load_parquet("my_data/files/files/1heart.csv.parquet")

if df.empty:
    print("Файл данных пустой или не существует.")
else:
    print(f"Данные загружены: {df.head()}")

chart_type = "scatter"
x_column = "Sex"
y_column = "Age"
title = "Пример графика"

if chart_type == "scatter":
    fig = px.scatter(df, x=df['Sex'], y=df['Age'], title=title)
elif chart_type == "line":
    fig = px.line(df, x=df['Sex'], y=df['Age'], title=title)
elif chart_type == "bar":
    fig = px.bar(df, x=df['Sex'], y=df['Age'], title=title)
elif chart_type == "pie":
    fig = px.pie(df, names=x_column, values=y_column, title=title)

fig.show()
