from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    # current_club 프로퍼티에 현재 속하는 Club 리턴
    #

class Club(models.Model):
    name = models.CharField(max_length=40)
    players = models.ManyToManyField(
        Player,
        through='TradeInfo',
    )

    def __str__(self):
        return self.name


class TradeInfo(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    date_joined = models.DateField()
    date_leaved = models.DateField(null=True, blank=True)

    # property로 is_current 속성이 TradeInfo가 현재 현직(leaved하지 않았는지)
