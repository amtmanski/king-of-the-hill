from django.shortcuts import render, redirect
from .forms import MatchForm, EventForm
from .models import Match, Event, Player, FinalClassification


def index(request):
    return render(request, "tournament/index.html")

def create_match(request, event_id):
    event=Event.objects.get(pk=event_id)
    if request.method == 'POST':
        winner_id = request.POST.get('winner')
        winner = Player.objects.get(pk=winner_id)
        if not Match.objects.filter(event=event):
            match_number=1
            loser = event.player_1 if winner==event.player_2 else event.player_2
        else:
            last_match_number = max(list(Match.objects.filter(event=event).values_list('match_number', flat=True)))
            last_loser = Match.objects.get(event=event, match_number=last_match_number).loser
            loser = Player.objects.all().exclude(id__in=[last_loser.id, winner.id])[0]
            match_number = last_match_number + 1
        match = Match(event=event, winner=winner, loser=loser, match_number=match_number)
        match.save()
        players = Player.objects.all().exclude(id=loser.id)
        return render(request, 'tournament/create_match.html', {'event': event, 'players': players, "match_no":match_number+1})
    else:
        players = Player.objects.filter(id__in=[event.player_1.id,event.player_2.id])
        return render(request, 'tournament/create_match.html', {'event': event, 'players': players, "match_no":1})


def add_points(request, event_id):
    event=Event.objects.get(pk=event_id)
    classification = FinalClassification.objects.all()
    if not event.pts_in_general:
        matches = Match.objects.filter(event_id=event_id)
        wojti_pts = len(matches.filter(winner=Player.objects.get(name='Wojti')))
        barti_pts = len(matches.filter(winner=Player.objects.get(name='Barti')))
        mati_pts = len(matches.filter(winner=Player.objects.get(name='Mati')))
        d = {'Wojti':wojti_pts, 'Barti':barti_pts, 'Mati':mati_pts}
        sorted_dict = {k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True)}
        if sorted(d.items(), key=lambda item: item[1], reverse=True)[-2][1]==0 and sorted(d.items(), key=lambda item: item[1], reverse=True)[-2][1]==0:
            winner_pts = 2
        else:
            winner_pts = 1
        p0 = classification[0]
        p1 = classification[1]
        p2 = classification[2]
        p0.won_matches = p0.won_matches + sorted_dict[p0.player.name]
        p0.save()
        p1.won_matches = p1.won_matches + sorted_dict[p1.player.name]
        p1.save()
        p2.won_matches = p2.won_matches + sorted_dict[p2.player.name]
        p2.save()
        winner = FinalClassification.objects.get(player__name=sorted(d.items(), key=lambda item: item[1], reverse=True)[0][0])
        winner.points = winner.points + winner_pts
        winner.save()
        event.pts_in_general = True
        event.save()
    return render(request, 'tournament/final_classification.html', {'classification': classification})

def match_list(request, event_id):
    matches = Match.objects.filter(event_id=event_id)
    wojti_pts = len(matches.filter(winner=Player.objects.get(name='Wojti')))
    barti_pts = len(matches.filter(winner=Player.objects.get(name='Barti')))
    mati_pts = len(matches.filter(winner=Player.objects.get(name='Mati')))
    return render(request, 'tournament/match_list.html', {'matches': matches})

def start_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            event_id=event.id
            return redirect('create_match', event_id=event_id)
    else:
        form = EventForm()
    return render(request, 'tournament/start_event.html', {'form': form})


def final_classification(request):
    classification = FinalClassification.objects.all()
    return render(request, 'tournament/final_classification.html', {'classification': classification})