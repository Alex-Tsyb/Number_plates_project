from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.
# class CustomUser(AbstractUser):
#     email = models.EmailField(unique=True)

#     # Додаємо аргумент related_name для уникнення конфліктів
#     groups = models.ManyToManyField(
#         Group,
#         related_name='customuser_set',  # Унікальне ім'я для зв'язку груп
#         blank=True,
#         help_text='Групи, до яких належить цей користувач. Користувач отримає всі дозволи, надані кожній із груп.',
#         related_query_name='customuser',
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         related_name='customuser_set',  # Унікальне ім'я для зв'язку дозволів
#         blank=True,
#         help_text='Специфічні дозволи для цього користувача.',
#         related_query_name='customuser',
#     )

#     def __str__(self):
#         return self.username