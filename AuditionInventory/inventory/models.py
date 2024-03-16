from django.core.validators import MinValueValidator
from django.db import models


class BaseModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Supplier(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Product(BaseModel):
    name = models.CharField(max_length=255)
    product_supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.FileField(upload_to='product')
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    price = models.DecimalField(decimal_places=2, max_digits=12)

    def __str__(self):
        return self.name




