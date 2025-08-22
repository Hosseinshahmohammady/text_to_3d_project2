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
                'Authorization': f'Token {SKETCHFAB_API_TOKEN}'
            }
            params = {
                'q': prompt
            }
            response = requests.get(
                'https://api.sketchfab.com/v3/models',
                headers=headers,
                params={'search': prompt}
            )


            print("وضعیت پاسخ:", response.status_code)
            print("متن خام پاسخ:", response.text)

            if response.status_code == 200:
                try:
                    data = response.json()
                    results = data.get('results', [])
                    print("نوع داده‌ی results:", type(results))

                    if isinstance(results, list):
                        for item in results:
                            if isinstance(item, dict):
                                model_links.append({
                                    'name': item.get('name'),
                                    'url': item.get('viewerUrl'),
                                    'uid': item.get('uid')
                                })
                                print("مدل:", item.get('name'), "| UID:", item.get('uid'))
                            else:
                                print("⚠️ item رشته است، نه دیکشنری:", item)
                    else:
                        print("⚠️ results لیست نیست:", results)
                except Exception as e:
                    print("⚠️ خطا در تبدیل JSON:", e)
            else:
                print("⚠️ پاسخ ناموفق از API:", response.status_code)
    else:
        form = TextForm()

    return render(request, 'textto3d/search.html', {'form': form, 'models': model_links})
