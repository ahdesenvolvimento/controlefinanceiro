from django.contrib import admin
from .models import Base, Saldo, Adicao, Retirar, RegistroAdicao, RegistroRetirada, Despesas, RegistroDespesas, CustomUsuario
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UsuarioChangeForm, CreateAdminForm

@admin.register(CustomUsuario)
class CustomUsuarioAdmin(UserAdmin):
    add_form = CreateAdminForm
    form = UsuarioChangeForm
    model = CustomUsuario
    list_display = ('first_name', 'last_name', 'email', 'fone', 'is_staff')
    '''Dados de cadastro do usuário'''
    fieldsets = (
        (None, {'fields':('email','password')}),
        ('Informações Pessoais', {'fields':('first_name', 'last_name', 'fone')}),
        ('Permissões',{'fields':('is_active', 'is_staff', 'is_superuser', 'groups','user_permissions')}),
        ('Datas importantes',{'fields':('last_login', 'date_joined')})
    )

@admin.register(Saldo)
class SaldoAdmin(admin.ModelAdmin):
    list_display = ['cod_saldo', 'tipo', 'quantidade', 'criacao', 'modificacao', 'proprietario']

    def get_queryset(self, request):
        qs = super(SaldoAdmin, self).get_queryset(request)
        return qs.filter(proprietario=request.user)

    def save_model(self, request, obj, form, change):
        obj.autor = request.user
        super().save_model(request, obj, form, change)

@admin.register(Adicao)
class AdicionarAdmin(admin.ModelAdmin):
    list_display = ['cod_adicao', 'quantidade', 'destino', 'criacao', 'modificacao']


@admin.register(Retirar)
class RetirarAdmin(admin.ModelAdmin):
    list_display = ['cod_retirada', 'quantidade', 'motivo', 'vem_de_onde', 'criacao', 'modificacao']

@admin.register(RegistroAdicao)
class RegirstroADDAdmin(admin.ModelAdmin):
    list_display = ['cod_adicao', 'cod_saldo']

'''
    def get_queryset(self, request):
        qs = super(RegirstroADDAdmin, self).get_queryset(request)
        return qs.filter(proprietario=request.user)

    def save_model(self, request, obj, form, change):
        obj.autor = request.user
        super().save_model(request, obj, form, change)
'''
@admin.register(RegistroRetirada)
class RegistroRetirarAdmin(admin.ModelAdmin):
    list_display = ['cod_retirada', 'cod_saldo']

@admin.register(Despesas)
class DespesasAdmin(admin.ModelAdmin):
    list_display = ['cod_despesa', 'nome', 'descricao', 'total']

@admin.register(RegistroDespesas)
class RegistroDespesasAdmin(admin.ModelAdmin):
    list_display = ['cod_retirada', 'cod_despesa']