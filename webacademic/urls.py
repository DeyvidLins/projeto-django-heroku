"""webacademic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from academic import views
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.views.generic import RedirectView
from . import settings

urlpatterns = [

    path('admin/', admin.site.urls),
    path('home/', views.inicio),
    path('login-aluno/', views.login_user_aluno),
    path('logout/', views.logout_user),
    path('portal-aluno/<int:username>/', views.portal_aluno),
    path('login-aluno/submit', views.login_submit_aluno),
    path('situacao-aluno/', views.situacao_al),
    path('boletim/', views.aluno_boletim),
    path('login-professor/',views.login_user_professor), # Professor
    path('login-professor/submit', views.login_submit_professor), # Professor
    path('portal-professor/<int:username>/', views.portal_professor), # Professor
    path('registro-notas/',views.registro_notas), # Professor
    path('', RedirectView.as_view(url='home/')),
    path('disciplinas/',views.disciplina_turma),  # Professor
    path('listar-alunos/',views.lista_alunos),  # Professor
    path('lancamento/', views.lancamento),  # Professor
    path('lancamento-nota/<int:id_disc>/<int:cpf_prof>/',views.lancamento_notas),
    path('nota-delete/',views.notas_delete),
    path('delete/',views.delete),
    path('nota-update/',views.notas_update),
    path('update/', views.update),
    path('image-perfil/',views.image_perfil),

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
