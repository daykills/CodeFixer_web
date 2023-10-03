from django.shortcuts import render
from django.contrib import messages


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
    return render(request, 'home.html', {'lang_list': lang_list})
