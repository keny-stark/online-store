from django.db import models
product_status_choices = [('monitors', 'monitors'), ('processors', 'processors'),
                          ('other', 'other'), ('video card', 'video card'),
                          ('components', 'components'), ('laptops', 'laptops'),
                          ('motherboards', 'motherboards'), ('RAM', 'RAM'),
                          ('cooling systems', 'cooling systems'), ('power supplies', 'power supplies'),
                          ('cases', 'cases')]


class Products(models.Model):
    name = models.TextField(max_length=100, null=False, blank=False, verbose_name='Name')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Description')
    status = models.TextField(max_length=40, null=False, blank=False,
                              choices=product_status_choices, default='other', verbose_name='Status')
    balance = models.IntegerField(verbose_name='Balance')
    price = models.DecimalField(max_digits=7, verbose_name='Price', decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
