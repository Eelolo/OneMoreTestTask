from django.db import models


class Company(models.Model):
    """Model that represents a company and its type of ownership"""

    OOO = 'ООО'
    OAO = 'ОАО'
    ZAO = 'ЗАО'
    PAO = 'ПАО'

    OWNERSHIP_TYPES = [
        (OOO, 'ООО'),
        (OAO, 'ОАО'),
        (ZAO, 'ЗАО'),
        (PAO, 'ПАО'),
    ]

    ownership = models.CharField(
        max_length=3, choices=OWNERSHIP_TYPES, default=OOO, verbose_name='Company ownership',
    )
    name = models.CharField(max_length=100, verbose_name='Company name')

    def __str__(self):
        return self.name
