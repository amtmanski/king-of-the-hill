from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Event(models.Model):
    date = models.DateField()
    arena = models.CharField(max_length=50)
    player_1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_1', null=True)
    player_2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_2',null=True)
    pts_in_general = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.date} {self.arena}"


class Match(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    match_number = models.IntegerField()
    winner = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='won_matches')
    loser = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='lost_matches')


class FinalClassification(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE)
    won_matches = models.IntegerField()
    points = models.IntegerField()