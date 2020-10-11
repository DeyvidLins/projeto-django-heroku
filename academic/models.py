from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User


# Create your models here.
class Escola(models.Model):
    cnpj = models.AutoField(primary_key=True)
    nome_escola = models.CharField(max_length=200)
    endereco = models.TextField()
    telefone = models.CharField(max_length=10)

    def __str__(self):
       return str(self.nome_escola)

class Turma(models.Model):
    cod_turma = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=60)
    turno = models.CharField(max_length=10)
    cpnj_escola = models.ForeignKey(Escola, on_delete=models.CASCADE)

    def __str__(self):
       return str(self.nome)

class Professor(models.Model):
    cpf_professor = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200)
    salario = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
       return str(self.nome)

class Disciplina(models.Model):
    id_disciplina = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=30)
    carga_horaria = models.IntegerField()
    cod_turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    cpf_professor = models.ForeignKey(Professor, on_delete=models.CASCADE)

    def __str__(self):
       return str(self.nome)

class Responsavel(models.Model):
    cpf_resp = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200)
    dt_nascimento = models.DateField()

    def __str__(self):
       return str(self.nome)


class Aluno(models.Model):
    cpf = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200)
    dt_nascimento = models.DateField()
    foto = models.ImageField(upload_to='perfil', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cod_turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    cpf_resp =  models.ForeignKey(Responsavel, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.nome)


class Situacao_aluno(models.Model):
    id_disciplina = models.ForeignKey(Disciplina,on_delete=models.CASCADE)
    cpf = models.ForeignKey(Aluno,on_delete=models.CASCADE)
    nota = models.CharField(max_length=4, null=True)
    frequencia = models.IntegerField(null=True)

    def __str__(self):
       return str(self.id_disciplina)