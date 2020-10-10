from django.contrib import admin
from .models import Aluno,Responsavel, Escola, Professor, Turma, Situacao_aluno, Disciplina


# Register your models here.
@admin.register(Aluno)
class alunoAdmin(admin.ModelAdmin):
    list_display = ['cpf', 'nome']

@admin.register(Responsavel)
class respAdim(admin.ModelAdmin):
    list_display = ['cpf_resp', 'nome']

@admin.register(Escola)
class escolAdim(admin.ModelAdmin):
    list_display = ['cnpj', 'nome_escola']

@admin.register(Professor)
class profAdim(admin.ModelAdmin):
    list_display = ['cpf_professor', 'nome']

@admin.register(Turma)
class turAdim(admin.ModelAdmin):
    list_display = ['cod_turma', 'nome']

@admin.register(Situacao_aluno)
class sitAdim(admin.ModelAdmin):
    list_display = ['cpf', 'nota']

@admin.register(Disciplina)
class discAdim(admin.ModelAdmin):
    list_display = ['nome', 'carga_horaria']


