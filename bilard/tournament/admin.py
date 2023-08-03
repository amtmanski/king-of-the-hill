from django.contrib import admin
from tournament.models import Player, FinalClassification
# Register your models here.
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    
@admin.register(FinalClassification)
class FinalClassificationAdmin(admin.ModelAdmin):
    list_display = ['player', 'won_matches', 'points']