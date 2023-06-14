import pickle
from tsfresh import extract_features, select_features
from tsfresh.utilities.dataframe_functions import make_forecasting_frame
from tsfresh.utilities.dataframe_functions import impute
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import plotly.graph_objects as go
import math


def get_model(path):
    with open(f'{path}', 'rb') as f:
        model = pickle.load(f)

    return model


def make_prediction(new_data, model):
    # Подсчитайте количество бронирований по месяцам
    df = new_data.groupby('date')['id'].count().reset_index()

    # Убираем пропущенные месяцы
    df = df[(df['date'] < '2021-11-01') | (df['date'] > '2022-02-01')]

    df_shift, y = make_forecasting_frame(df['id'], kind="count", max_timeshift=10, rolling_direction=1)

    # Извлекаем признаки
    X = extract_features(df_shift, column_id="id", column_sort="time", column_value="value", impute_function=impute,
                         show_warnings=False)

    # Предсказание на новых данных
    y_pred = model.predict(X)

    # Оцениваем модель
    mse = mean_squared_error(y, y_pred)
    rmse = math.sqrt(mse)
    mae = mean_absolute_error(y, y_pred)
    r2 = r2_score(y, y_pred)

    # print(f"MSE: {mse}")
    # print(f"RMSE: {rmse}")
    # print(f"MAE: {mae}")
    # print(f"R2 Score: {r2}")

    # Создаем график
    # fig = go.Figure()

    # Добавляем линии для фактических и прогнозируемых значений
    # fig.add_trace(go.Scatter(x=df.date, y=y, mode='lines', name='Actual'))
    # fig.add_trace(go.Scatter(x=df.date, y=y_pred, mode='lines', name='Predicted'))

    # Показываем график
    # fig.show()

    return y_pred