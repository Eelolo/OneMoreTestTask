from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


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


class Deal(models.Model):
    """A model that represents a deal with a contact"""

    name = models.CharField(max_length=100, verbose_name='Deal name')
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, verbose_name='Contact', related_name='deals')

    def __str__(self):
        return self.name


class DealStage(models.Model):
    """A model that represents the stage of the deal and the probability of its success"""

    name = models.CharField(max_length=100, verbose_name='Deal stage name', db_index=True)
    probability = models.IntegerField(
        verbose_name='Probability of success (0-100%)', db_index=True,
        validators=[
            MinValueValidator(0, message='Value must be greater than 0'),
            MaxValueValidator(100, message='Value must be less than 100')
        ]
    )

    def __str__(self):
        return self.name
