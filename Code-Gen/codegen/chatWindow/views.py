import json
from django.http import JsonResponse
from django.shortcuts import render
from transformers import pipeline,AutoTokenizer, AutoModelForCausalLM
import requests
import os

# Create your views here.

#to load the wizard model uncomment the code bellow and comment the salesforce model code and EleutherAI model as well<-------
#load the model
#pipe = pipeline("text-generation", model="WizardLMTeam/WizardCoder-Python-34B-V1.0")


#--->to load the salesforce model uncomment the code bellow and comment the EleutherAI model code<-------
#salesforce model
#pipe = pipeline("text-generation", model="Salesforce/codegen-16B-mono")


# Salesforce CodeGen-6B-mono model (activated)
# tokenizer = AutoTokenizer.from_pretrained("Salesforce/codegen-6B-mono")
# model = AutoModelForCausalLM.from_pretrained("Salesforce/codegen-6B-mono")
# pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

# # EleutherAI model
# tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")
# model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B")
# pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Load the Salesforce CodeGen-2B-mono model directly
tokenizer = AutoTokenizer.from_pretrained("Salesforce/codegen-2B-mono")
model = AutoModelForCausalLM.from_pretrained("Salesforce/codegen-2B-mono")
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

def index(request):
    return render(request, 'chatWindow/index.html')

# uncomment bellow if you are using salesforce model or wizardcoder model
# code for using salesforce model and wizard model
# def generate_code(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         prompt = data.get('prompt', '')

#         # Generate code from the prompt using the loaded model
#         generated_code = pipe(prompt, max_length=200, do_sample=True)[0]['generated_text']

#         return JsonResponse({'generated_code': generated_code})
#     return JsonResponse({'error': 'Invalid request'}, status=400)


# #Lazy loading of the model
# def generate_code(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         prompt = data.get('prompt', '')

#         # Load model when needed
#         tokenizer = AutoTokenizer.from_pretrained("Salesforce/codegen-6B-mono")
#         model = AutoModelForCausalLM.from_pretrained("Salesforce/codegen-6B-mono")
#         pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

#         generated_code = pipe(prompt, max_length=200, do_sample=True)[0]['generated_text']

#         return JsonResponse({'generated_code': generated_code})
#     return JsonResponse({'error': 'Invalid request'}, status=400)


#comment the bellow code if you are not using EleutherAI model
# code for using EleutherAI model and salesforce 2b model
def generate_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        prompt = data.get('prompt', '')

        # Generate code from the prompt using the loaded model
        generated_code = pipe(prompt, max_length=500, do_sample=True, top_k=50, truncation=True)[0]['generated_text']

        return JsonResponse({'generated_code': generated_code})
    return JsonResponse({'error': 'Invalid request'}, status=400)




#vllm code if using wizard model different way to load the model

# def generate_code(prompt):
#     url = "http://localhost:8000/v1/chat/completions"
#     headers = {"Content-Type": "application/json"}
#     data = {
#         "model": "WizardLMTeam/WizardCoder-Python-34B-V1.0",
#         "messages": [{"role": "user", "content": prompt}]
#     }
#     response = requests.post(url, headers=headers, json=data)
#     return response.json()