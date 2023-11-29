from django.db import models


# model for catogery managment
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# model for product details 
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Unisex', 'Unisex')],
        default='Unisex'
    )
    status = models.BooleanField(default=True)
    

    def __str__(self):
        return self.name
    
    
# model for product images
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    
    def __str__(self):
        return f'Images for {self.product.name}'


# model for product variants 
class SizeVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    quantity = models.PositiveIntegerField(null=False, default=0)
    price = models.PositiveIntegerField(null=False, default=0)
    discount_percent = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.product.name} - {self.size}"


class Banner(models.Model):
    BANNER_TYPES = (
        ('main_banner', 'Main Banner'),
        ('mini_banner_left', 'Mini Banner Left'),
        ('mini_banner_center', 'Mini Banner Center'),
        ('mini_banner_right', 'Mini Banner Right'),
    )

    main_title = models.CharField(max_length=250, null=False)
    subtitle = models.CharField(max_length=250, default='03', blank=True,)
    file_input = models.ImageField(upload_to='banners/',default='0', null=False)
    banner_type = models.CharField(max_length=20, choices=BANNER_TYPES, default='main_banner', null=False)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.main_title
    
