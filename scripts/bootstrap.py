# Bootstraps the Roots instance with the default
# set of the necessary objects

import datetime

site = Site.objects.get_current()

competition = Competition(
  name="Sample competition",
  site=site
)

competition.save()

problemset_series_1 = ProblemSet(
    name="Problems in the first series",
    competition=competition
)
problemset_series_1.save()

season = Season(
    competition=competition,
    name="First season",
    year=datetime.date.today().year,
    number=1,
    start=datetime.datetime.now(),
    end=datetime.datetime.now()+datetime.timedelta(days=30),
    problemset=problemset_series_1
)
season.save()

series = Series(
   season=season,
   name="First series",
   number=1,
   submission_deadline=datetime.datetime.now()+datetime.timedelta(days=30)
)
series.save()
