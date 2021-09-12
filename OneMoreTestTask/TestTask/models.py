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


class Contact(models.Model):
    """A model that represents a contact and its affiliation with a particular company"""

    first_Name = models.CharField(max_length=100, verbose_name='First name')
    last_Name = models.CharField(max_length=100, verbose_name='Last mame')
    patronymic = models.CharField(max_length=100, verbose_name='Patronymic')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Company', related_name='contacts')

    def __str__(self):
        return f'{self.first_Name} {self.last_Name} {self.patronymic}'
