from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    ordem = models.IntegerField()

    def __str__(self):
        return self.nome
    
class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14)
    datanasc = models.DateField(null=True, blank=True)

    @property
    def datanascimento(self):
        if self.datanasc:
            return self.datanasc.strftime('%d/%m/%Y')
        return None

    def __str__(self):
        return self.nome
    
class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14)
    datanasc = models.DateField(null=True, blank=True)

    @property
    def datanascimento(self):
        if self.datanasc:
            return self.datanasc.strftime('%d/%m/%Y')
        return None
    
class Produto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nome
    
class Pedido(models.Model):

    STATUS_CHOICES = (
        (1, 'Novo'),
        (2, 'Em andamento'),
        (3, 'Finalizado'),
        (4, 'Cancelado'),
    )

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data = models.DateField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Pedido {self.id}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.produto.nome

class Estoque(models.Model):
    produto = models.OneToOneField(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=0)

    def __str__(self):
        return self.produto.nome



