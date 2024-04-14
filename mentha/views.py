import base64

from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.utils.http import urlsafe_base64_encode

from .forms import ContactoForm
from .models import Noticia

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.encoding import smart_str

# Create your views here.

char_map = {
    smart_str("+º", encoding='utf-8', strings_only=True, errors='strict'): smart_str("ç", encoding='utf-8',
                                                                                     strings_only=True,
                                                                                     errors='strict'),
    smart_str("+ú", encoding='utf-8', strings_only=True, errors='strict'): smart_str("ã", encoding='utf-8',
                                                                                     strings_only=True,
                                                                                     errors='strict'),
    smart_str("+¬", encoding='utf-8', strings_only=True, errors='strict'): smart_str("é", encoding='utf-8',
                                                                                     strings_only=True,
                                                                                     errors='strict'),
    smart_str("+¦", encoding='utf-8', strings_only=True, errors='strict'): smart_str("ó", encoding='utf-8',
                                                                                     strings_only=True,
                                                                                     errors='strict'),
    smart_str("+¬", encoding='utf-8', strings_only=True, errors='strict'): smart_str("ê", encoding='utf-8',
                                                                                     strings_only=True,
                                                                                     errors='strict'),
    smart_str("+é", encoding='utf-8', strings_only=True, errors='strict'): smart_str("Â", encoding='utf-8',
                                                                                     strings_only=True,
                                                                                     errors='strict'),
    smart_str("+Ò", encoding='utf-8', strings_only=True, errors='strict'): smart_str("é", encoding='utf-8',
                                                                                     strings_only=True,
                                                                                     errors='strict'),
    smart_str("+í", encoding='utf-8', strings_only=True, errors='strict'): smart_str("á", encoding='utf-8',
                                                                                     strings_only=True,
                                                                                     errors='strict'),
    smart_str("+¡", encoding='utf-8', strings_only=True, errors='strict'): smart_str("í", encoding='utf-8',
                                                                                     strings_only=True,
                                                                                     errors='strict'),
    smart_str("+á", encoding='utf-8', strings_only=True, errors='strict'): smart_str("à", encoding='utf-8',
                                                                                     strings_only=True,
                                                                                     errors='strict'),
    smart_str("+ë", encoding='utf-8', strings_only=True, errors='strict'): smart_str("É", encoding='utf-8',
                                                                                     strings_only=True,
                                                                                     errors='strict'),
    smart_str("+ü", encoding='utf-8', strings_only=True, errors='strict'): smart_str("Á", encoding='utf-8',
                                                                                     strings_only=True,
                                                                                     errors='strict'),
    smart_str("+ó", encoding='utf-8', strings_only=True, errors='strict'): smart_str("â", encoding='utf-8',
                                                                                     strings_only=True,
                                                                                     errors='strict'),
}


def replace_chr(text):
    if text is not None:
        smart_txt = smart_str(text, encoding='utf-8', strings_only=True, errors='strict')
        for incorrect_char, correct_char in char_map.items():
            smart_txt = text.replace(incorrect_char, correct_char)
        return smart_txt
    return text


import django.apps


def decode():
    app_models = django.apps.apps.get_models()
    for model in app_models:
        for field in model._meta.get_fields():
            if field.name == 'id':
                continue

            if field.get_internal_type() in ['CharField', 'TextField']:
                instances = model.objects.exclude(**{field.name: ''})

                for instance in instances:
                    old_value = getattr(instance, field.name)
                    new_value = replace_chr(old_value)
                    setattr(instance, field.name, new_value)
                    instance.save()

    return None


def login_page_view(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponse('ok')
        else:
            return HttpResponse('nok')

    return render(request, 'mentha/login.html')


def logout_page_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('mentha:index'))


def index_page_view(request):
    return render(request, 'mentha/base.html')


def home_page_view(request):  # mudar o nome para intro
    return render(request, 'mentha/index.html')


def projeto_page_view(request):
    return render(request, 'mentha/projeto.html')


def aplicacoes_page_view(request):
    return render(request, 'mentha/aplicacoes.html')


def mentha_cog_page_view(request):
    return render(request, 'mentha/mentha-cog.html')


def mentha_care_page_view(request):
    return render(request, 'mentha/mentha-care.html')


def protocolo_mentha_page_view(request):
    return render(request, 'mentha/protocolo-mentha.html')


def parceiros_page_view(request):
    return render(request, 'mentha/parceiros.html')


def equipa_page_view(request):
    return render(request, 'mentha/equipa.html')


def noticias_page_view(request):
    return render(request, 'mentha/noticias.html', {
        'noticias': Noticia.objects.all().order_by('-data')
    })


def videoconferencia_page_view(request):
    return render(request, 'mentha/videoconferencia.html')


def zoom_div_page_view(request):
    return render(request, 'mentha/zoom-div.html')


def contacto_page_view(request):
    print('\n\nEntrou em contacto. request.POST:', request.POST)

    form = ContactoForm(request.POST or None)

    if form.is_valid():
        print(f'form valido, vai gravar: {request.POST["nome"]}')
        form.save()
        form = ContactoForm(None)
        return render(request, 'mentha/contacto.html', {
            'form': form,
            'mensagem': 'Obrigado pela sua mensagem!'
        })

    return render(request, 'mentha/contacto.html', {
        'form': form
    })


def app_list_view(request):
    show = []
    if request.user.groups.filter(name__in=['Mentor', 'Cuidador', 'Administrador']).exists():
        show.append('CARE')
    if request.user.groups.filter(name__in=['Dinamizador', 'Participante', 'Administrador']).exists():
        show.append('COG')
    if request.user.groups.filter(name__in=['Avaliador', 'Administrador', 'Avaliador-Risk']).exists():
        show.append('Protocolo')

    context = {
        'show': show,
    }
    return render(request, 'mentha/app-list.html', context)


def forgot_password(request):
    email = request.POST.get('email')

    if not email:
        return render(request, 'mentha/forgot.html', {'error': 'Por favor, insira o seu email.'})

    users = User.objects.filter(email=email)

    if not users.first():
        return render(request, 'mentha/forgot.html', {'error': 'O email inserido não está registado.'})

    for user in users:
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(user.pk.to_bytes(4, 'big'))

        reset_link = request.build_absolute_uri(f'/resetar/{uidb64}/{token}/')

        send_mail(
            'Definição de palavra chave',
            f'Olá,\n\nPediu para redefinir a sua palavra chave para o username: {user.username}, clique por favor no '
            f'seguinte link:\n\n{reset_link}',
            'info.menthadigital@gmail.com',
            [email]
        )

    return render(request, 'mentha/forgot.html',
                  {'success': 'Foi-lhe enviado um email com um link para redefinir a sua senha.'})


def password_reset_confirm(request, uidb64, token):
    try:
        uid = base64.urlsafe_b64decode(uidb64 + '==')
        uid = int.from_bytes(uid, 'big')

        user = User.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                form = SetPasswordForm(user, request.POST)
                if form.is_valid():
                    form.save()
                    return render(request, 'mentha/password_reset_confirm.html',
                                  {'success': 'A sua senha foi redifinida com sucesso!','token': token, 'uidb64': uidb64})
            else:
                form = SetPasswordForm(user)
            return render(request, 'mentha/password_reset_confirm.html',
                          {'form': form, 'token': token, 'uidb64': uidb64, 'username': user.username})
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        pass

    form = SetPasswordForm(user)
    return render(request, 'mentha/password_reset_confirm.html',
                  {'form': form, 'token': token, 'uidb64': uidb64, 'username': user.username})
