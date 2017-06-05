from django.db import models


class Topping(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Pizza(models.Model):
    name = models.CharField(max_length=30)
    toppings = models.ManyToManyField(Topping)

    def __str__(self):
        # 자신이 가지고 있는 토핑목록을 뒤에 출력
        return '{} 피자의 재료: {}'.format(self.name, ', '.join([topping.name for topping in self.toppings.all()]))

    class Meta:
        ordering = ('name',)
