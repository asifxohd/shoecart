from django.db import models


# your code goes here 

# model for catogery managment
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# model for product details 
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # Gender as a boolean field (e.g., True for Male, False for Female)
    gender = models.BooleanField()
    theme_image = models.ImageField(upload_to='product_images/')
    side_image_1 = models.ImageField(upload_to='product_images/')
    side_image_2 = models.ImageField(upload_to='product_images/')
    side_image_3 = models.ImageField(upload_to='product_images/')
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# model for product variants 
class SizeVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.size}"
