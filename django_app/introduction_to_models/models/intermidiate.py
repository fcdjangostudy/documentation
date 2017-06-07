from django.db import models
from django.db.models import Q  # 장고 filter에서 and or 연산을 쓰고 싶을 때 사용
from datetime import datetime


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
    # @property
    # def current_tradeinfo(self):
    #     whoami = TradeInfo.objects.get(
    #         player=self.id,
    #         date_leaved=None
    #     )
    #     return '{}, 현 {} 소속, {} 입단'.format(whoami.player, whoami.club, whoami.date_joined)

    @property
    def current_tradeinfo(self):
        return self.tradeinfo_set.get(
            date_leaved__isnull=True)  # null은 데이터베이스 상 없다는 뜻, none은 파이썬 상 없다는 뜻 그러나 쿼리상으로는 뜻이 둘 다 같다.


class Club(models.Model):
    name = models.CharField(max_length=40)
    players = models.ManyToManyField(
        Player,
        through='TradeInfo',
        through_fields=('club', 'player')
    )

    def __str__(self):
        return self.name

    def squad(self, year=None):
        if year:
            return self.players.filter(
                Q(tradeinfo__date_leaved__gt=datetime(year + 1, 1, 1)) &
                Q(tradeinfo__date_joined__lte=datetime(year, 12, 31))
            )
        else:
            return self.players.filter(
                tradeinfo__date_leaved__isnull=True,
            )  # 현직 선수만 가져오기


class TradeInfo(models.Model):
    # recommender = models.ForeignKey(Player, on_delete=models.CASCADE)
    # prev_club = 이전 Club

    # 1. property로 is_current 속성이 TradeInfo가 현재 현직(leaved하지 않았는지)여부 반환
    # 2. recommender와 prev_club을 활성화시키고 Club의 MTM필드에 through_fields를 명시

    # 위의 요구조건들을 만족하는 실행코드 작성

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    date_joined = models.DateField()
    date_leaved = models.DateField(null=True, blank=True)
    recommender = models.ForeignKey(
        Player,
        on_delete=models.PROTECT,
        related_name='tradeinfo_recommender',  # Manager의 이름을 새롭게 지정함.
        null=True,
        blank=True,
    )
    prev_club = models.ForeignKey(
        Club,
        on_delete=models.PROTECT,
        related_name='tradeinfo_prev_club',
        # Manager의 이름을 새롭게 지정함.(역참조하는 RelatedManager의 이름을 변경, 다른 참조부분과 이름이 겹치기 때문이다.)
        null=True,
        blank=True,
    )

    def __str__(self):
        # return '{} {} {} {} ~ {}'.format(self.player.id, self.player, self.club, self.date_joined, self.date_leaved)
        return '{}, {} ({}~{})'.format(
            self.player,
            self.club,
            self.date_joined,
            self.date_leaved if self.date_leaved else '현직',  # self.date_leaved or '현직'
        )

    @property
    def is_current(self):
        return not self.date_leaved  # reutrn self.date_leaved is None
