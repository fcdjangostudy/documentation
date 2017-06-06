from django.db import models
from django.utils import timezone
from django.utils.datetime_safe import date


class Player(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    # current_club프로퍼티에 현재 속하는 Club리턴
    @property
    def current_club(self):
        return self.club_set.get(
            tradeinfo__date_leaved__exact=None
        )

    # current_tradeinfo프로퍼티에 현재 자신의 TradeInfo리턴
    @property
    def current_tradeinfo(self):
        whoami = TradeInfo.objects.get(
            player=self.id,
            date_leaved=None
        )
        return '{}, 현 {} 소속, {} 입단'.format(whoami.player, whoami.club, whoami.date_joined)


class Club(models.Model):
    name = models.CharField(max_length=40)
    players = models.ManyToManyField(
        Player,
        through='TradeInfo',
    )
    prev_club = models.ManyToManyField(
        Player,
        through='TradeInfo',
        through_fields=('Player', 'Club'),
        related_name='_related',

    )

    def __str__(self):
        return self.name

    def squad(self, year=None):
        if year:
            return ', '.join([info.player.name for info in
                              TradeInfo.objects.filter(
                                  club__id=self.id,
                                  date_joined__gte=date(year, 1, 1),
                                  date_joined__lte=date(year, 12, 31),
                              )])
        else:
            return ', '.join([info.player.name for info in
                              TradeInfo.objects.filter(
                                  club__id=self.id,
                                  date_joined__gte=date(timezone.datetime(year), 1, 1),
                                  date_joined__lte=date(timezone.datetime(year), 12, 31),
                                  date_leaved=None,
                              )])


class TradeInfo(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    date_joined = models.DateField()
    date_leaved = models.DateField(null=True, blank=True)
    recommender = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    prev_club = models.ForeignKey(
        Club,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return '{} {} {} {} {}'.format(self.player.id, self.player, self.club, self.date_joined, self.date_leaved)

        # recommender = models.ForeignKey(Player, on_delete=models.CASCADE)
        # prev_club = 이전 Club

        # 1. property로 is_current 속성이 TradeInfo가 현재 현직(leaved하지 않았는지)여부 반환
        # 2. recommender와 prev_club을 활성화시키고 Club의 MTM필드에 through_fields를 명시

        # 위의 요구조건들을 만족하는 실행코드 작성

    @property
    def is_current(self):
        return self.date_leaved is None
