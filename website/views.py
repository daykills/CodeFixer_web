from django.shortcuts import render


def home(request):
    lang_list = ['c', 'clike', 'cpp', 'csharp', 'css', 'dart', 'django', 'go',
                 'java', 'javascript', 'jsx', 'markup', 'markup-templating',
                 'matlab', 'mongodb', 'perl', 'php', 'python', 'r', 'sql',
                 'swift', 'yaml']
    print(request.method)

    if request.method == 'POST':
        lang = request.POST['lang']
        code = request.POST['code']
        print(lang, code)
        return render(request, 'home.html', {'lang': lang, 'code': code,
                                             'lang_list': lang_list})
    return render(request, 'home.html', {'lang_list': lang_list})
