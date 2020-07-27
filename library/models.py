from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Member(models.Model):
    owner = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    contact = models.CharField(max_length=17, blank=True)
    address = models.CharField(max_length=10000, null=False)
    due = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "Member Table"


class BookDetail(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    book_name = models.CharField(max_length=1000000, default="NULL")

    def __str__(self):
        return "Book Detail Table"


class Publisher(models.Model):
    name = models.CharField(max_length=1000)
    book_name = models.CharField(max_length=10000, unique=True)
    number_of_book = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "Publisher Table"
