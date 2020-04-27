from django.shortcuts import render, redirect, HttpResponse
from .models import Saldo, Adicao, Retirar, Despesas
from .forms import AdicionarModelForm, RetirarModelForm, DespesasModelForm
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import connection
# Create your views here.
def IndexView(request):
    if str(request.user) != 'AnonymousUser':
        #print(request.user)
        if str(request.method == 'POST'):
            with connection.cursor() as cursor:
                #cursor.execute('SELECT * FROM core_adicao_conta')
                #print(request.user.email)
                #cursor.execute('SELECT ca.quantidade, ca.destino, ca.criacao, cs.quantidade, cs.quantidade-ca.quantidade FROM core_adicao ca INNER JOIN core_saldo cs ON cs.tipo = ca.destino INNER JOIN core_customusuario cu ON cs.proprietario_id = cu.id')
                #cursor.execute('SELECT CA.quantidade, CA.destino, CA.criacao, CS.quantidade-CA.quantidade, CS.quantidade FROM CORE_CUSTOMUSUARIO CU INNER JOIN CORE_SALDO CS ON ID = CS.PROPRIETARIO_ID INNER JOIN CORE_REGISTROADICAO RA ON ID = RA.PROPRIETARIO_ID INNER JOIN CORE_ADICAO CA ON CA.DESTINO = CS.TIPO WHERE CU.EMAIL = %s', (request.user.email, ))
                cursor.execute('SELECT CA.quantidade, CA.destino, CA.criacao, CS.quantidade FROM CORE_CUSTOMUSUARIO CU INNER JOIN CORE_SALDO CS ON CU.ID = CS.PROPRIETARIO_ID INNER JOIN CORE_REGISTROADICAO RA ON CS.COD_SALDO = RA.COD_SALDO_ID INNER JOIN CORE_ADICAO CA ON RA.COD_ADICAO_ID = CA.COD_ADICAO WHERE CU.EMAIL = %s', (request.user.email, ))
                linha = cursor.fetchall()
                cursor.execute('SELECT TIPO, QUANTIDADE, CU.ID, PROPRIETARIO_ID FROM CORE_SALDO INNER JOIN CORE_CUSTOMUSUARIO CU ON CU.ID = PROPRIETARIO_ID WHERE CU.ID = %s', (request.user.id, ))
                dados = cursor.fetchall()
                total = 0
                for i in dados:
                    total += i[1]

            return render(request, 'index.html', {'valores':linha, 'dados':dados, 'total':total})
    else:
        return redirect('contas/login')

        '''
        #valores = RetirarValor.objects.all()
        valores = AdicionarValor.objects.all()

        qnt = Saldo.objects.all()#(tipo=primeiro.destino)

        context = {'valores':valores,
                   'qnt':qnt}
        total = 0
        #lista = []
        for i in qnt:
            total += i.quantidade
        context['total'] = total
        '''
        #return render(request, 'index.html', {'valores':linha})

def adicionar(request):
    if str(request.method == 'POST'):
        with connection.cursor() as cursor:
            form = AdicionarModelForm(request.POST)
            saldos = Saldo.objects.all()
            #cursor.execute('SELECT TIPO, QUANTIDADE FROM CORE_SALDO')
            #dados = cursor.fetchall()

            if form.is_valid():
                dados = form.cleaned_data
                sald = Saldo.objects.filter(proprietario=request.user.id).filter(tipo=dados['destino'])
                sald = sald.first()
                print(sald)
                #print(sald.proprietario.get(proprietario=request.user.id))
                #cursor.execute('SELECT * FROM CORE_SALDO CS WHERE CS.TIPO = %s AND CS.PROPRIETARIO_ID = %s', (dados['destino'], request.user.id))
                #sald = cursor.fetchall()
                #print(sald[0][4])
                #print(dados, sald.tipo, dados['destino'])
                if sald.tipo == dados['destino'] and sald.proprietario_id == request.user.id:
                    #print(dados, sald.tipo, dados['destino'])
                    sald.quantidade = float(sald.quantidade) + float(dados['quantidade'])
                    sald.save()
                    form.save()
                    ultima_adicao = Adicao.objects.filter().last()
                    #cursor.execute('SELECT * FROM core_registroadicao')
                    #for i in cursor.fetchall():
                      #  print(type(i), i)
                    cursor.execute('INSERT INTO core_registroadicao (cod_adicao_id, cod_saldo_id, criacao, modificacao) VALUES (%s, %s, %s, %s)', (ultima_adicao.cod_adicao, sald.cod_saldo, sald.criacao, ultima_adicao.modificacao, ))
                    connection.close()
                    connection.commit()
                    print(type(ultima_adicao.cod_adicao), ultima_adicao.quantidade)
                    print(type(sald.cod_saldo))
                return redirect('index')
            else:
                print('Não é valido')
            return render(request, 'adicionar.html', {'tipos':saldos})



def retirar(request):
    if str(request.method == 'POST'):
        with connection.cursor() as cursor:
            saldos = Saldo.objects.all()
            form = RetirarModelForm(request.POST)
            if form.is_valid():
                #try:
                dados = form.cleaned_data
                if ('Conta' or 'conta') in dados['motivo']:
                    print('tem contad')
                    #try:
                    # except ObjectDoesNotExist:
                    #  print('eoq2')
                    despesa = Despesas.objects.filter(proprietario=request.user.id).filter(nome=dados['motivo'])
                    despesa = despesa.first()
                    print('to aqui', '1', despesa)
                    sald = Saldo.objects.get(tipo=dados['vem_de_onde'])
                    print()
                    if dados['vem_de_onde'] == sald.tipo and sald.quantidade > 0 and sald.quantidade >= dados['quantidade']:
                        sald.quantidade = float(sald.quantidade) - float(dados['quantidade'])
                        despesa.total = float(despesa.total) - float(dados['quantidade'])
                        despesa.save()
                        sald.save()
                        form.save()
                        ultima_retirada = Retirar.objects.filter().last()
                        #print(ultima_retirada.cod_retirada, sald.cod_saldo, sald.criacao, ultima_retirada.modificacao)
                        cursor.execute(
                            'INSERT INTO core_registroretirada (cod_retirada_id, cod_saldo_id, criacao, modificacao) VALUES (%s, %s, %s, %s)',
                            (ultima_retirada.cod_retirada, sald.cod_saldo, sald.criacao, ultima_retirada.modificacao,))
                        connection.close()
                        connection.commit()
                    else:
                        print('aqui agora')
                    #return redirect('index')
                else:
                    sald = Saldo.objects.filter(tipo=dados['vem_de_onde']).filter(proprietario=request.user.id)
                    sald = sald.first()
                    if dados['vem_de_onde'] == sald.tipo and sald.quantidade > 0 and sald.quantidade >= dados['quantidade']:
                        sald.quantidade = float(sald.quantidade) - float(dados['quantidade'])
                        sald.save()
                        form.save()
                        ultima_retirada = Retirar.objects.filter().last()
                        #print(ultima_retirada.cod_retirada, sald.cod_saldo, sald.criacao, ultima_retirada.modificacao)
                        cursor.execute(
                            'INSERT INTO core_registroretirada (cod_retirada_id, cod_saldo_id, criacao, modificacao) VALUES (%s, %s, %s, %s)',
                            (ultima_retirada.cod_retirada, sald.cod_saldo, sald.criacao, ultima_retirada.modificacao,))
                        connection.close()
                        connection.commit()
                    return redirect('index')
                #except:
                 #   return HttpResponse('Ops')
            else:
                print('eoq')
        return render(request, 'retirar.html',{'tipos':saldos})


def despesa(request):
    if str(request.POST == 'POST'):
        form = DespesasModelForm(request.POST)
        despesas = Despesas.objects.all()
        if form.is_valid():
            form.save()
    return render(request, 'despesas.html', {'despesas':despesas})