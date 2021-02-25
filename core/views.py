from django.shortcuts import render, redirect
from .forms import ContatoForm, ProdutoModelForm
from django.contrib import messages
from .models import Produto


def index(request):
    context = {'produtos': Produto.objects.all()}
    return render(request, 'index.html', context)


def contato(request):
    form_contato = ContatoForm(request.POST or None)  # POST = formulário preenchido, GET = formulário vazio

    if request.method == 'POST':
        if form_contato.is_valid():  # verifica se o formulário foi devidamente preenchido e se o token é válido
            # nome = form_contato.cleaned_data['nome']  # pega valor da chave no dicionário cleaned_data
            # email = form_contato.cleaned_data['email']
            # assunto = form_contato.cleaned_data['assunto']
            # mensagem = form_contato.cleaned_data['mensagem']

            # print(f'{nome}, {email}, {assunto}, {mensagem}')

            form_contato.send_mail()

            messages.success(request, 'Mensagem enviada com sucesso!')  # envia mensagem de sucesso
            form_contato = ContatoForm()  # limpa o formulário
        else:
            messages.error(request, 'Erro ao enviar mensagem!')  # envia mensagem de erro

    return render(request, 'contato.html', {'form_contato': form_contato})


def produto(request):
    # if str(request.user) == 'AnonymousUser':  # maneira ensinada no curso
    if not request.user.is_authenticated:  # usando atributo de user - mais elegante
        return redirect('index')
    else:
        if request.method == 'POST':
            form_produto = ProdutoModelForm(request.POST, request.FILES)
            if form_produto.is_valid():
                form_produto.save()
                messages.success(request, 'Sucesso!')
            else:
                messages.error(request, 'Erro!')

        form_produto = ProdutoModelForm()

        return render(request, 'produto.html', {'form_produto': form_produto})

