import json
import requests
from django.http import JsonResponse
from django.shortcuts import render

def index(request):
    return render(request, 'chatWindow/index.html')

def generate_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        prompt = data.get('prompt', '')

        try:
            # Send a POST request to the model API
            api_url = "http://localhost:5000/generate-code"  # FastAPI URL
            response = requests.post(api_url, json={"prompt": prompt})
            response_data = response.json()

            if response.status_code == 200:
                return JsonResponse({'generated_code': response_data.get('generated_code', '')})
            else:
                return JsonResponse({'error': response_data.get('detail', 'Unknown error')}, status=response.status_code)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': f'Error connecting to model API: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)
