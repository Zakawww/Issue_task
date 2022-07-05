from django.db import models



other_choice = 'other'
category_choices = [
    (other_choice, 'Other'),
    ('notebooks', 'Notebooks'),
    ('computers', 'Computers'),
    ('monitors', 'Monitors')
]


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Description')
    category = models.CharField(max_length=30, choices=category_choices, default=other_choice, verbose_name='Category')
    count = models.PositiveIntegerField(default=0, verbose_name='Balance')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Price')

    def __str__(self):
        return f'{self.name} - {self.category} - {self.price}'

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

