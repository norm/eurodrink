from datetime import date
from django.core.management.base import BaseCommand
import toml

from contests.models import (
    Language,
    Country,
    Contest,
    Singer,
    Artist,
    Song,
    Participant,
    Show,
    Performance,
    Score,
)
from incidents.models import (
    PerformanceIncidentType,
    PerformanceIncident,
    ScoreIncidentType,
    ShowIncidentType,
)

class Command(BaseCommand):
    help = 'Import from eurovision_data/ files'

    def handle(self, *args, **options):
        self.load_performance_incident_types('drinking_data/performance.toml')
        self.load_score_incident_types('drinking_data/score.toml')
        self.load_show_incident_types('drinking_data/show.toml')

        self.load_countries('eurovision_data/countries.toml')
        self.load_contests('eurovision_data/contests.toml')

        for contest in Contest.objects.all():
            self.load_singers('eurovision_data/singers/%s.toml' % contest.year)
            self.load_artists('eurovision_data/artists/%s.toml' % contest.year)
            self.load_songs('eurovision_data/songs/%s.toml' % contest.year, contest)
            self.load_shows('eurovision_data/shows/%s.toml' % contest.year, contest)

        for show in Show.objects.all():
            self.load_scores(
                'eurovision_data/scores/%s-%s.toml' % (
                    show.contest.year,
                    show.type,
                ),
                show,
            )

        for contest in Contest.objects.all():
            self.load_show_incidents('drinking_data/%s.toml' % contest.year, contest)

    def load_countries(self, data):
        countries = toml.load(data)
        for country in countries:
            langs = []
            for language in countries[country]['language']:
                lang, _ = Language.objects.get_or_create(id=language)
                langs.append(lang)
            del countries[country]['language']
            obj, _ = Country.objects.update_or_create(
                id=country,
                **countries[country],
            )
            for lang in langs:
                obj.languages.add(lang)

    def load_contests(self, data):
        contests = toml.load(data)
        for contest in contests:
            Contest.objects.update_or_create(
                year=contest,
                host=Country.objects.get(id=contests[contest]['host']),
            )

    def load_singers(self, data):
        singers = toml.load(data)
        for singer in singers:
            citizenships = singers[singer].pop('citizenship')
            obj, _ = Singer.objects.update_or_create(
                id=singer,
                **singers[singer],
            )
            for country in citizenships:
                obj.citizenship.add(Country.objects.get(id=country))

    def load_artists(self, data):
        artists = toml.load(data)
        for artist in artists:
            singers = artists[artist].pop('singer')
            obj, _ = Artist.objects.update_or_create(
                id=artist,
                **artists[artist],
            )
            for singer in singers:
                obj.singer.add(Singer.objects.get(id=singer))

    def load_songs(self, data, contest):
        songs = toml.load(data)
        for song in songs:
            langs = []
            country = Country.objects.get(id=songs[song]['country'])
            for language in songs[song]['language']:
                lang, _ = Language.objects.get_or_create(id=language)
                langs.append(lang)
            obj, _ = Song.objects.update_or_create(
                id=song,
                title=songs[song]['title'],
                artist=Artist.objects.get(id=songs[song]['artist']),
                country=country,
                contest=contest,
            )
            for lang in langs:
                obj.languages.add(lang)

            # a Participant is a Country in a Contest, which has a 1:1
            # relationship with a Song, so we create that here too
            Participant.objects.get_or_create(
                country=country,
                contest=contest,
            )

    def load_shows(self, data, contest):
        another = PerformanceIncidentType.objects.get(id='another-country')
        langchange = PerformanceIncidentType.objects.get(id='language-change')

        shows = toml.load(data)
        for show in shows:
            in_past = shows[show]['date'] < date.today()
            show_obj, _ = Show.objects.update_or_create(
                id=show,
                contest=contest,
                type=shows[show]['type'],
                date=shows[show]['date'],
            )
            for performance in shows[show]['performances']:
                perf_obj, _ = Performance.objects.update_or_create(
                    song=Song.objects.get(id=performance),
                    show=show_obj,
                    occurred=in_past,
                )
                # since we have the data for this already, add draft incidents
                # for "singer from another country" and "language change"
                if not in_past and show_obj.type == 'final':
                    for singer in perf_obj.song.artist.singer.all():
                        for cs in singer.citizenship.all():
                            if perf_obj.song.country != cs:
                                PerformanceIncident.objects.create(
                                    type=another,
                                    performance=perf_obj,
                                    predicted=True,
                                )
                if perf_obj.song.languages.count() > 1:
                    PerformanceIncident.objects.create(
                        type=langchange,
                        performance=perf_obj,
                        predicted=True,
                    )

    def load_scores(self, data, show):
        try:
            scores = toml.load(data)
        except:
            print('** no scores for %s' % show)
            return

        for country_id in scores:
            country = Country.objects.get(id=country_id)
            for score in scores[country_id]:
                performance = Performance.objects.filter(
                    show=show,
                    song=Song.objects.get(id=score['song']),
                )[0]
                Score.objects.update_or_create(
                    performance=performance,
                    country=country,
                    points=score['points'],
                    source=score['source'],
                )

    def load_performance_incident_types(self, data):
        incidents = toml.load(data)
        for incident in incidents:
            PerformanceIncidentType.objects.update_or_create(
                id=incident,
                **incidents[incident],
            )

    def load_score_incident_types(self, data):
        incidents = toml.load(data)
        for incident in incidents:
            ScoreIncidentType.objects.update_or_create(
                id=incident,
                **incidents[incident],
            )

    def load_show_incident_types(self, data):
        incidents = toml.load(data)
        for incident in incidents:
            ShowIncidentType.objects.update_or_create(
                id=incident,
                **incidents[incident],
            )

    def load_show_incidents(self, data, contest):
        try:
            incidents = toml.load(data)
        except:
            print('** no incidents for %s' % contest)
            return

        show = contest.show_set.get(type='final')
        future = show.date >= date.today()
        for song_id in incidents:
            # print(song_id, incidents[song_id])
            for incident in incidents[song_id]:
                incident_type = PerformanceIncidentType.objects.get(id=incident)
                performance = Performance.objects.filter(
                    song=song_id,
                    show=show,
                )[0]
                PerformanceIncident.objects.create(
                    type=incident_type,
                    performance=performance,
                    predicted=future,
                )
