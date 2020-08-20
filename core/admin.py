from django.contrib import admin
from .models import Produto


@admin.register(Produto)  # registra Produto usando decoradores
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'estoque', 'slug', 'imagem', 'criado', 'modificado', 'ativo')


# admin.site.register(Produto)  # outra maneira de registrar models
