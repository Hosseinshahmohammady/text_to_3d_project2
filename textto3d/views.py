from django.shortcuts import render
from .forms import TextForm
import requests


SKETCHFAB_API_TOKEN = 'db6c4cf57537445c9bb55df893c274ec'

def text_view(request):
    model_links = []
    if request.method == 'POST':
        form = TextForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            headers = {
                'Authorization': f'Token {'db6c4cf57537445c9bb55df893c274ec'}'
            }
            params = {
                'q': prompt,
                'downloadable': True,
                'license': 'CC0'
            }
            response = requests.get('https://api.sketchfab.com/v3/search', headers=headers, params=params)
            if response.status_code == 200:
                results = response.json().get('results', [])
                for item in results:
                    model_links.append({
                        'name': item['name'],
                        'url': item['viewerUrl'],
                        'uid': item['uid']  # برای نمایش در iframe
                    })
    else:
        form = TextForm()
    return render(request, 'modelviewer/search.html', {'form': form, 'models': model_links})
