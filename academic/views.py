from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Aluno, Situacao_aluno, Professor, Disciplina
from .utils import render_to_pdf


def inicio(request):  # Inicia na página principal
    return render(request, 'home.html')


def login_user_aluno(request):
    return render(request, 'login-aluno.html')


def logout_user(request):  # Volta para a pagina principal home.html
    logout(request)
    return redirect('/home/')


@login_required(login_url='/login-aluno/')
def portal_aluno(request, username):  # View da html portal do perfil
    alunos = Aluno.objects.all().select_related("cpf_resp", "cod_turma", "user").filter(cpf=username)
    return render(request, 'image-perfil.html', {'alunos': alunos, "user": username})

def image_perfil(request):
    if request.POST:
        cpf_aluno = request.POST.get('cpf')
        foto = request.FILES.get('photo')
        aluno = Aluno.objects.get(cpf=cpf_aluno)
        if foto: #Caso seja uma foto(FILE), salva no banco
           aluno.foto = foto
        aluno.save()
        alunos = Aluno.objects.all().filter(cpf=cpf_aluno)
        return render(request, 'image-perfil.html', {'alunos': alunos})



@login_required(login_url='/login-aluno/')
def aluno_boletim(request):
    if request.POST:
        username = request.POST.get('name')
        print(username)
        situacao = Situacao_aluno.objects.all().select_related("cpf", "id_disciplina").filter(cpf=username)
        pdf = render_to_pdf('boletim.html', {'situacao': situacao})
        return HttpResponse(pdf, content_type='application/pdf')
    '''  return render(request, 'boletim.html', {'situacao': situacao})'''



@login_required(login_url='/login-aluno/')
def situacao_al(request):  # View situação perfil
    if request.POST:
        user = request.POST.get('user')
        username = request.POST.get('username')
        situacao = Situacao_aluno.objects.all().select_related("cpf", "id_disciplina").filter(cpf=username)
        sit = []
        for i in situacao:
            sit.append(i)
        return render(request, 'situacao-aluno.html', {"situacao": sit, "situ": i, "user": user})


@csrf_protect
def login_submit_aluno(request):  # Através da pagina login-aluno.html, com o botão entrar, verifica se o usuário está cadastrado no sistema, caso não esteja mostra uma mensagem.
    if request.POST:
        username = request.POST.get('username')
        senha = request.POST.get('password')
        user = authenticate(username=username, password=senha)
        if user is not None:
            login(request, user)
            return redirect(f'/portal-aluno/{username}/')

        else:
            messages.error(request, 'Usuário ou senha inválida. Favor tentar novamente')

    return redirect('/login-aluno/')


def login_user_professor(request):
    return render(request, 'login-professor.html')


@csrf_protect
def login_submit_professor(request):
    if request.POST:
        username = request.POST.get('username')
        senha = request.POST.get('password')
        user = authenticate(username=username, password=senha)
        if user is not None:
            login(request, user)
            return redirect(f'/portal-professor/{username}/')

        else:
            messages.error(request, 'Usuário ou senha inválida. Favor tentar novamente')

    return redirect('/login-professor/')


@login_required(login_url='/login-professor/submit')
def portal_professor(request,username):  # View da html portal do perfil
    prof = Professor.objects.all().select_related("user").filter(cpf_professor=username)
    return render(request, 'portal-professor.html', {'prof': prof})


@login_required(login_url='/login-professor/')
def registro_notas(request):  # Lançamento das notas dos alunos
    if request.POST:
        cpf_prof = request.POST.get('prof')
        disc = Disciplina.objects.all().select_related("cod_turma", "cpf_professor").filter(cpf_professor=cpf_prof)
        return render(request, 'registro-notas.html', {"disc": disc, "cpf_prof":cpf_prof})


@login_required(login_url='/login-professor/')
def disciplina_turma(request):  # pagina disciplinas.html
    cpf_prof = request.POST.get('prof')
    id_disc = request.POST.get('turma')
    disc = Disciplina.objects.all().select_related("cod_turma", "cpf_professor").filter(id_disciplina=id_disc)
    disciplina = id_disc
    return render(request, 'disciplinas.html', {"disc": disc, "disci": disciplina,"cpf_prof":cpf_prof})


@login_required(login_url='/login-professor/')
def lista_alunos(request):  # lista os alunos cadastrados da turmas para lançamento das notas
    if request.POST:
        cpf_prof = request.POST.get('prof')
        id_disc = request.POST.get('id_disc')
        cod_turm = request.POST.get('cod_turma')
        disc = Disciplina.objects.all().select_related("cod_turma").filter(cod_turma=cod_turm)
        al = Aluno.objects.all().select_related("cod_turma").filter(cod_turma=cod_turm)
        return render(request, 'listar-alunos.html', {"al": al, "disc": disc, "disciplina": id_disc,"cpf_prof":cpf_prof})


@login_required(login_url='/login-professor/')
def lancamento(request):  # Insere as notas e faltas no banco de dados
    if request.GET:
        cpf_prof = request.GET.get('prof')
        id_disc = request.GET.get('id_disc')
        disciplina = Disciplina.objects.get(id_disciplina=id_disc)  # Chave estrangeira de situacao_aluno
        cpf_aluno = request.GET.getlist('cpf')
        nota = request.GET.getlist('nota')
        freq = request.GET.getlist('freq')
        cont = 0
        for cpf in cpf_aluno:
            aluno = Aluno.objects.get(cpf=cpf)
            Situacao_aluno.objects.create(id_disciplina=disciplina, cpf=aluno, nota=nota[cont], frequencia=freq[cont])
            cont += 1
      #  import pdb; pdb.set_trace()  #  Depurador
        url = (f'/lancamento-nota/{id_disc}/{cpf_prof}/')
    return redirect(url)  # enviando um id com a url


@login_required(login_url='/login-professor/')
def lancamento_notas(request, id_disc,cpf_prof):
    disc = Disciplina.objects.all().select_related("cod_turma")
    sit = Situacao_aluno.objects.all().select_related("cpf", "id_disciplina").filter(id_disciplina=id_disc)
    return render(request, 'lanc-notas.html', {"sit": sit, "disc": disc ,"id_disc":id_disc, "cpf_prof": cpf_prof})


def notas_delete(request):
    if request.POST:
      cpf_prof = request.POST.get('prof')
      id_disc =request.POST.get('id_disc')
      disc = Disciplina.objects.all()
      sit = Situacao_aluno.objects.all()
      return render(request, 'delete-notas.html', {"sit": sit, "disc": disc, "id_disc":id_disc,"cpf_prof": cpf_prof})


def delete(request):
    if request.POST:
        cpf_prof = request.POST.get('prof')
        id_disc = request.POST.get('id_disc')
        nome = request.POST.get('nome')
        cpf_aluno = request.POST.get('cpf')
      
        aluno_sit = Situacao_aluno.objects.get(cpf=cpf_aluno)
        aluno_sit.delete()

        disc = Disciplina.objects.all()
        sit = Situacao_aluno.objects.all()
        msg = (f'Notas e faltas deletadas do aluno {nome}')
     
        return render(request, 'delete-notas.html', {"sit": sit, "disc": disc, "id_disc":id_disc,"cpf_prof": cpf_prof,"msg": msg})

def notas_update(request):
    if request.POST:
        cpf_prof = request.POST.get('prof')
        id_disc = request.POST.get('id_disc')
        disc = Disciplina.objects.all()
        sit = Situacao_aluno.objects.all()
        return render(request, 'update-notas.html', {"sit": sit, "disc": disc, "id_disc": id_disc, "cpf_prof":cpf_prof})

def update (request):
    if request.POST:
        cpf_prof = request.POST.get('prof')
        id_disc = request.POST.get('id_disc')
        cpf_aluno = request.POST.getlist('cpf')
        nota = request.POST.getlist('nota')
        freq = request.POST.getlist('freq')
        cont = 0
        for cpf in cpf_aluno:
            aluno = Situacao_aluno.objects.get(cpf=cpf)
            aluno.nota = nota[cont]
            aluno.freq = freq[cont]
            aluno.save()
            cont += 1

        disc = Disciplina.objects.all()
        sit = Situacao_aluno.objects.all()
        msg = ('Notas atualizadas com Sucesso!')
        return render(request, 'update-notas.html', {"sit": sit, "disc": disc,"id_disc": id_disc,"cpf_prof": cpf_prof, "msg": msg})



