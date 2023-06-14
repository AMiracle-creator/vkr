from django import forms


class AgeClustersForm(forms.Form):
    min_age = forms.IntegerField(min_value=1)
    max_age = forms.IntegerField(max_value=100)


class HotelInfoForm(forms.Form):
    hotel_id = forms.IntegerField(min_value=1)


class DateForm(forms.Form):
    first_day = forms.CharField()
    first_month = forms.CharField()
    first_year = forms.CharField()
    second_day = forms.CharField()
    second_month = forms.CharField()
    second_year = forms.CharField()
