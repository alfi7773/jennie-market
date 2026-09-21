from django.db import models


class Category(models.Model):

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['id']

    title = models.CharField('название', max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Material(models.Model):

    class Meta:
        verbose_name = 'материал'
        verbose_name_plural = 'материалы'
        ordering = ['id']

    title = models.CharField('название', max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class Color(models.Model):

    class Meta:
        verbose_name = 'цвет'
        verbose_name_plural = 'цвета'
        ordering = ['id']

    title = models.CharField('название', max_length=50, unique=True)
    hex_code = models.CharField('HEX-код', max_length=7, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Корзина {self.id}"


class CartItem(models.Model):
    cart = models.ForeignKey(
        'jennie.Cart',
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        'jennie.Product',
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    quantity = models.PositiveIntegerField(
        default=1
    )


    def total_price(self):
        return self.product.price * self.quantity


    def __str__(self):
        return f"{self.product.title} - {self.quantity}"

class Product(models.Model):

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['-created_at']

    title = models.CharField('название', max_length=50)
    price = models.DecimalField('цена', max_digits=10, decimal_places=2)
    care = models.TextField('уход и стирка')
    compound = models.TextField('состав')
    country = models.CharField('страна бренда', max_length=90)
    description = models.TextField('описание товара')
    category = models.ForeignKey('jennie.Category', on_delete=models.PROTECT, related_name="products")
    colors = models.ManyToManyField('jennie.Color', related_name='products')
    material = models.ForeignKey('jennie.Material', on_delete=models.PROTECT, related_name="products")
    image = models.ImageField('изображение', upload_to='products/', blank=True, null=True)
    is_new = models.BooleanField('новинка',default=False)
    is_sale = models.BooleanField('скидка',default=False)
    is_trend = models.BooleanField('в тренде',default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title


class Contact(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    phone = models.CharField(max_length=20,verbose_name="Телефон")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

# Create your models here.
