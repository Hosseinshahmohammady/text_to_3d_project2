from django import forms

class TextForm(forms.Form):
    prompt = forms.CharField(lable='متن خود را وارد بکنید', max_length=100)