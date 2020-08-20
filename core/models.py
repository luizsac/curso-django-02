from django.db import models
from stdimage.models import StdImageField
from django.db.models import signals  # envia sinal sobre modificações no modelo "observado"
from django.template.defaultfilters import slugify  # cria endereço personalizado com base no nome do objeto

class Base(models.Model):
    criado = models.DateField('Data de Criação', auto_now_add=True)
    modificado = models.DateField('Data de Modificação', auto_now=True)
    ativo = models.BooleanField('Ativo', default=True)

    class Meta:  # adiciona opções de metadados à classe
        abstract = True  # define a classe como abstrata para que não seja persistida no banco


class Produto(Base):
    nome = models.CharField('Nome', max_length=100)
    preco = models.DecimalField('Preço', max_digits=8, decimal_places=2)
    estoque = models.IntegerField('Estoque')
    imagem = StdImageField('Imagem', upload_to='produtos', variations={'thumb': (124, 124)})
    slug = models.SlugField('Slug', max_length=100, blank=True, editable=False)

    def __str__(self):
        return self.nome


# função que deverá ser executada antes de uma instância de Produto seja persistida no banco
def produto_pre_save(signal, instance, sender, **kwargs):
    instance.slug = slugify(instance.nome)  # transforma 'Playstation 4 Slim' em 'playstation-4-slim', por exemplo


# conecta função pre_save com a classe Produto e a chama antes de uma instância de Produto ser persistida no banco
signals.pre_save.connect(produto_pre_save, sender=Produto)
