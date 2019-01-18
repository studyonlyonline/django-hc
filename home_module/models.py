from django.db import models

#schemes table for showing SCHEMES
class Schemes(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    image_url = models.TextField(default=None)
    title = models.CharField(max_length=255)
    seo_name = models.CharField(max_length=255, blank=True, null=True)
    terms_and_conditions = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

#Category table
class Category(models.Model):
    category_name = models.TextField()
    seo_name = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.category_name + " - " + self.seo_name + " - " + str(self.id)


# Product variants
class Variants(models.Model):
    variant_name = models.CharField(max_length=255)
    variant_value = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        if self.is_active:
            return self.variant_name + " -  " + self.variant_value
        else:
            return "NOT ACTIVE " + self.variant_name


class Products(models.Model):
    product_category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    mapped_variant = models.ManyToManyField(Variants)
    product_name  = models.TextField()
    product_seo_name = models.TextField(null=True)
    product_mrp = models.IntegerField(null=True)
    product_discount = models.FloatField(default=0)
    product_quantity = models.IntegerField(default=0)
    product_description = models.TextField(default=None)
    product_features = models.TextField(default=None)
    product_image_url = models.TextField(default=None)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product_name + " - qty ( " + str(self.product_quantity) + ") - cat (" + str(self.product_category.id) + ")"



