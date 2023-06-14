import json

import numpy as np
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from main.forms.search_froms import AgeClustersForm, HotelInfoForm, DateForm
from main.services.analytics.hotels_info import make_age_clusters, get_hotel, get_period_info
from main.services.ml.catboost_model_service import get_model, make_prediction
from main.services.read_csv.read_dataset import read_dataset


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


class HomePage(TemplateView):
    template_name = "main/index.html"


class AnalyticsPage(TemplateView):
    template_name = "main/analytics_page.html"


class PredictionPage(TemplateView):
    template_name = "main/predict.html"


def analytics_page(request):
    if request.method == 'GET':

        return render(request, 'main/analytics_page.html')

    if request.method == 'POST':
        form = AgeClustersForm(request.POST)
        print('not_valid')
        if form.is_valid():
            print('valid')
            min_age = form.cleaned_data['min_age']
            max_age = form.cleaned_data['max_age']

            df = read_dataset('media/tatarstan_hotels.csv')
            age_clusters = make_age_clusters(df, min_age, max_age)
            context = {"dataset": age_clusters}

            return render(request, 'main/analytics_page.html', context)

        context = {'error': ''}

        return render(request, 'main/analytics_page.html', context)


def indetifier_form(request):
    data = json.load(request)

    if data:
        print(data)
        hotel_id = int(data.get('hotel_id'))
        print(hotel_id)

        df = read_dataset('media/tatarstan_hotels.csv')
        hotel = get_hotel(df, hotel_id)
        context = {'hotel': hotel}
        print(json.dumps(context, cls=NpEncoder, ensure_ascii=False))

        return HttpResponse(json.dumps(context, cls=NpEncoder, ensure_ascii=False),
                            content_type="application/json", status=200)


def age_form(request):
    data = json.load(request)

    if data:
        min_age = data.get('min_age')
        max_age = data.get('max_age')


        df = read_dataset('media/tatarstan_hotels.csv')
        age_clusters = make_age_clusters(df, min_age, max_age)
        context = {'dataset': age_clusters}
        print(json.dumps(context, cls=NpEncoder, ensure_ascii=False))

        return HttpResponse(json.dumps(context, cls=NpEncoder, ensure_ascii=False),
                            content_type="application/json", status=200)


def date_form(request):
    data = json.load(request)

    if data:
        from_date = data.get('from_date')
        to_date = data.get('to_date')

        df = read_dataset('media/correct_statinfo.csv')
        total, date, date_amount = get_period_info(df, from_date, to_date)
        context = {'total': total, 'date': date, 'date_amount': date_amount}

        return HttpResponse(json.dumps(context, cls=NpEncoder, ensure_ascii=False),
                            content_type="application/json", status=200)


def single_hotel_info(request):
    if request.method == 'POST':
        form = HotelInfoForm(request.POST)

        if form.is_valid():
            hotel_id = form.cleaned_data['hotel_id']
            print(hotel_id)

            df = read_dataset('media/tatarstan_hotels.csv')
            hotel = get_hotel(df, hotel_id)
            context = {'hotel': hotel}

            return render(request, 'main/analytics_page.html', context)

    context = {'error': ''}

    return render(request, 'main/analytics_page.html', context)


def period_info(request):
    if request.method == 'POST':
        form = DateForm(request.POST)
        print('not_valid')
        if form.is_valid():
            print('valid')
            first_day = form.cleaned_data['first_day']
            first_month = form.cleaned_data['first_month']
            first_year = form.cleaned_data['first_year']

            first_date = f'{first_year}-{first_month}-{first_day}'

            second_day = form.cleaned_data['second_day']
            second_month = form.cleaned_data['second_month']
            second_year = form.cleaned_data['second_year']

            second_date = f'{second_year}-{second_month}-{second_day}'

            df = read_dataset('media/correct_statinfo.csv')
            total, date, date_amount = get_period_info(df, first_date, second_date)
            context = {'total': total, 'date': date, 'date_amount': date_amount}

            return render(request, 'main/analytics_page.html', context)

    context = {'error': ''}

    return render(request, 'main/analytics_page.html', context)


def predict(request):
    if request.method == 'GET':
        model = get_model('media/catboost_model.pkl')
        df = read_dataset('media/statinfo_for_model.csv')
        prediction = make_prediction(df, model)
        context = {
                   'predict_data': prediction
                   }

        return render(request, 'main/predict.html', context)
