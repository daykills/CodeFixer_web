from django.shortcuts import render,redirect
from django.contrib import messages
import openai
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from .models import Code

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
                # save to db
                record = Code(question=code, code_answer=response,
                              language=lang, user=request.user)
                record.save()
                return render(request, 'home.html', {'lang': lang,
                                                     'response': response,
                                                     'lang_list': lang_list})
                
            except Exception as e:
                return render(request, 'home.html', {'lang': lang, 'code': code,
                                                'lang_list': lang_list,
                                                'response': e})


    return render(request, 'home.html', {'lang_list': lang_list})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in.")
            return redirect('home')
        else:
            messages.success(request, "Error logging in. Try again.")
            return redirect('home')
    return render(request, 'home.html', {})
    
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

def signup_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print(form.is_valid())

        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have been registered.")
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'signup_user.html', {"form": form})


def history(request):
    if request.user.is_authenticated:
        records = Code.objects.filter(user_id=request.user.id)
        return render(request, 'history.html', {'records': records})
    else:
        messages.success(request, "You Must Be Logged In To View This Page")
        return redirect('home')


def delete_history(request, record_id):
    history_id = Code.objects.get(pk=record_id)
    history_id.delete()
    messages.success(request, "Deleted successfully")
    return redirect('home')
