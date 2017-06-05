from django.contrib import admin
from .models import Person, Player, Club, TradeInfo

admin.site.register(Person)
admin.site.register(Player)
admin.site.register(Club)
admin.site.register(TradeInfo)