from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Kategoriya nomi')
    image = models.ImageField(upload_to='categories/', null=True, blank=True, verbose_name='Rasm')
    slug = models.SlugField(unique=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategory',
                               verbose_name='Kategoriya')

    def get_photo(self):
        if self.image:
            try:
                return self.image.url
            except:
                return 'https://png.pngtree.com/element_our/20200702/ourlarge/pngtree-no-photo-icon-free-image_2292041.jpg'
        return 'https://png.pngtree.com/element_our/20200702/ourlarge/pngtree-no-photo-icon-free-image_2292041.jpg'

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('category_list', kwargs={'slug': self.slug})


    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'

class Product(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name="Mahsulot nomi")
    price = models.FloatField(verbose_name="Narxi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan vaqti")
    quantity = models.IntegerField(default=5, verbose_name="Ombordagi soni")
    description = models.TextField(default="Bu yerda tez orada ma'lumot bo'ladi!", verbose_name="Batafsil")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Kategoriya')
    slug = models.SlugField(unique=True, null=True)
    size = models.IntegerField(default=30, verbose_name="O'lcham mmda")
    colour = models.CharField(max_length=35, verbose_name='Rangi/Material', choices=[
        ('gold', 'Tilla'),
        ('silver', "Kumush"),
        ('bronze', 'Bronza')
    ])

    def get_photo(self):
        if self.images:
            try:
                return self.images.all()[0].image.url
            except:
                return 'https://png.pngtree.com/element_our/20200702/ourlarge/pngtree-no-photo-icon-free-image_2292041.jpg'
        return 'https://png.pngtree.com/element_our/20200702/ourlarge/pngtree-no-photo-icon-free-image_2292041.jpg'


    class Meta:
        verbose_name = 'Mahsulot'
        verbose_name_plural = 'Mahsulotlar'

class Gallery(models.Model):
    image = models.ImageField(upload_to='products/', verbose_name='Rasmlar')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = 'Mahsulot rasmi'
        verbose_name_plural = 'Mahsulot rasmlari'


class Review(models.Model):
    text = models.TextField(verbose_name='Izohingizni qoldiring...')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Avtor')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Mahsulot')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    publish = models.BooleanField(default=True)

    def __str__(self):
        return self.text[:20]

    class Meta:
        verbose_name = 'Izoh'
        verbose_name_plural = 'Izohlar'


class FavouriteProducts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Foydalanuvhci')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Mahsulot')

    def __str__(self):
        return f"{self.username} - {self.product.title}"

    class Meta:
        verbose_name = "Yoqtirgan mahsulot"
        verbose_name_plural = "Yoqtirgan mahsulotlar"


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()

    class Meta:
        verbose_name = 'Haridor'
        verbose_name_plural = 'Haridorlar'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    shipping = models.BooleanField(default=True)

    def __str__(self):
        return str(self.pk)

    @property
    def get_cart_total_price(self):
        order_products = self.orderproduct_set.all()
        total_price = sum([product.get_total_price for product in order_products])
        return total_price

    @property
    def get_cart_total_quantity(self):
        order_products = self.orderproduct_set.all()
        total_quantity = sum([product.quantity for product in order_products])
        return total_quantity

    class Meta:
        verbose_name = 'Buyurtma'
        verbose_name_plural = 'Buyurtmalar'


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_total_price(self):
        total_price = self.product.price * self.quantity
        return total_price


    class Meta:
        verbose_name = "Buyurtmadagi mahsulot"
        verbose_name_plural = "Buyurtmadagi mahsulotlar"


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=250, verbose_name='Adres')
    city = models.CharField(max_length=150, verbose_name='Shahar')
    state = models.CharField(max_length=250, verbose_name="Rayon")
    zipcode = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Adres'
        verbose_name_plural = 'Adreslar'



