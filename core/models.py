from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
# Create your models here.

class Base(models.Model):
    criacao = models.DateField('Criação', auto_now_add=True)
    modificacao = models.DateField('Modificado', auto_now=True)

    class Meta:
        abstract = True

class CustomManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('E-mail pfv!')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('is_staff tem quer ser = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser tem quer ser = True')
        return self._create_user(email, password, **extra_fields)

class CustomUsuario(AbstractUser):
    email = models.EmailField('Email', unique=True)
    fone = models.CharField('Telefone', max_length=15)
    is_staff = models.BooleanField('Membro', default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'fone']

    def __str__(self):
        return self.get_full_name()
    objects = CustomManager()

class Saldo(Base):
    UNITY_CHOICES = (
        ('Cofre', 'Cofre'),
        ('Passe', 'Passe'),
        ('Conta', 'Conta'),
    )
    cod_saldo = models.AutoField(primary_key=True)
    proprietario = models.ForeignKey(CustomUsuario, on_delete=models.CASCADE)
    tipo = models.CharField('Tipo do detalhe', max_length=70, choices=UNITY_CHOICES)
    quantidade = models.FloatField('Quantidade disponível')

    class Meta:
        verbose_name = 'Saldo'
        verbose_name_plural = 'Saldos'

    def __str__(self):
        return self.tipo

class Adicao(Base):
    cod_adicao = models.AutoField(primary_key=True)
    quantidade = models.FloatField('Quantidade para adicionar')
    destino = models.CharField('Destino',  max_length=20)

    class Meta:
        verbose_name = 'Adição'
        verbose_name_plural = 'Adições'

    def get_contas(self):
        return self.destino

class Retirar(Base):
    cod_retirada = models.AutoField(primary_key=True)
    quantidade = models.FloatField('Quantidade para retirar')
    motivo = models.CharField('Motivo', max_length=50)
    vem_de_onde = models.CharField('De onde vem', max_length=20)

    class Meta:
        verbose_name = 'Retirada'
        verbose_name_plural = 'Retiradas'

    def get_contas(self):
        return self.vem_de_onde
    

class Despesas(Base):
    cod_despesa = models.AutoField(primary_key=True)
    nome = models.CharField("Nome", max_length=50)
    descricao = models.TextField("Descrição", max_length=255)
    total = models.FloatField("Total em R$")
    #parcela = models.BooleanField()

    class Meta:
        verbose_name = 'Despesa'
        verbose_name_plural = 'Despesas'

    def __str__(self):
        return self.nome


class RegistroDespesas(Base):
    cod_registro_despesa = models.AutoField(primary_key=True)
    cod_despesa = models.ForeignKey(Despesas, on_delete=models.CASCADE)
    cod_retirada = models.ForeignKey(Retirar, on_delete=models.CASCADE)

class RegistroAdicao(Base):
    cod_registro = models.AutoField(primary_key=True)
    cod_adicao = models.ForeignKey(Adicao, on_delete=models.CASCADE)
    cod_saldo = models.ForeignKey(Saldo, on_delete=models.CASCADE)
    

class RegistroRetirada(Base):
    cod_registro = models.AutoField(primary_key=True)
    cod_retirada = models.ForeignKey(Retirar, on_delete=models.CASCADE)
    cod_saldo = models.ForeignKey(Saldo, on_delete=models.CASCADE)



