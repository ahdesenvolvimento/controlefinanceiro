from django import forms
from .models import Adicao, Retirar, Despesas, CustomUsuario
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
class AdicionarModelForm(forms.ModelForm):
    #destino = forms.MultipleChoiceField
    class Meta:
        model = Adicao
        #fields = ['quantidade', 'conta']
        exclude = ['cod_adicao']
        list_display = ['quantidade', 'destino']

class RetirarModelForm(forms.ModelForm):
    class Meta:
        model = Retirar
        exclude = ['cod_retirada']
        fields = ['quantidade', 'motivo', 'vem_de_onde']

class DespesasModelForm(forms.ModelForm):
    class Meta:
        model = Despesas
        exclude = ['cod_despesa']
        fields = ['nome', 'descricao', 'total']

class CreateAdminForm(UserCreationForm):
    class Meta:
        model = CustomUsuario
        fields = ('first_name', 'last_name', 'fone')
        labels = {'username': 'Username/E-mail'}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.email = self.cleaned_data['username']
        if commit:
            user.save()
        return user

class UsuarioChangeForm(UserChangeForm):
    class Meta:
        model = CustomUsuario
        fields = ('first_name', 'last_name', 'fone')

