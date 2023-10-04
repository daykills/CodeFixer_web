from django.shortcuts import render
from django.contrib import messages
import openai


def home(request):
    lang_list = ['c', 'clike', 'cpp', 'csharp', 'css', 'dart', 'django', 'go',
                 'java', 'javascript', 'jsx', 'markup', 'markup-templating',
                 'matlab', 'mongodb', 'perl', 'php', 'python', 'r', 'sql',
                 'swift', 'yaml']

    if request.method == 'POST':
        lang = request.POST['lang']
        code = request.POST['code']
        
        if lang == "Select Programming Languages":
            messages.success(request,
                             "You forgot to select a programming language")
            return render(request, 'home.html', {'lang': lang, 'code': code,
                                'lang_list': lang_list})
        else:
            openai.api_key = "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"
            openai.Model.list()
            try:
                response = openai.Completion.create(
                    engine='text-davinci-003',
                    prompt=f'Respond with code. Fix this {lang} code :{code}',
                    temperature=0,
                    max_tokens=1000,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                    )
                response = response['choices'][0]['text'].strip()
                return render(request, 'home.html', {'lang': lang,
                                                     'response': response,
                                                     'lang_list': lang_list})
                
            except Exception as e:
                return render(request, 'home.html', {'lang': lang, 'code': code,
                                                'lang_list': lang_list,
                                                'response': e})


    return render(request, 'home.html', {'lang_list': lang_list})

