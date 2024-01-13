from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Cat(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=1024)

    def __str__(self):
        return self.name


class Medal(models.Model):
    cat = models.ForeignKey(Cat,
                            on_delete=models.CASCADE,
                            related_name='medals')
    name = models.CharField(max_length=1024)
