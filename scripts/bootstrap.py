# Bootstraps the Roots instance with the default
# set of the necessary objects

import datetime

site = Site.objects.get_current()

# Create the admin user
admin = User.objects.create(
    username="rootsadmin",
    email="rootsadmin@example.com",
    is_staff=True,
    is_superuser=True,
)
admin.set_password('rootspassword')
admin.save()

# Verify his email
email = admin.emailaddress_set.get(pk=1)
email.verified = True
email.save()

# Add competition with 1 season composed of 1 series
# with its corresponding problem set
competition = Competition.objects.create(
    name="Sample competition",
    site=site
)

season = Season.objects.create(
    competition=competition,
    name="First season",
    year=datetime.date.today().year,
    number=1,
    start=datetime.datetime.now(),
    end=datetime.datetime.now()+datetime.timedelta(days=30),
)

problemset_series_1 = ProblemSet.objects.create(
    name="Problems in the first series",
    competition=competition
)

series = Series.objects.create(
   season=season,
   name="First series",
   number=1,
   submission_deadline=datetime.datetime.now()+datetime.timedelta(days=30),
   problemset=problemset_series_1
)

# Create a Facebook social provider
facebook = SocialApp.objects.create(
    provider="facebook",
    name="Facebook",
    client_id="random_client_id",
    secret="random_secret",
)
facebook.sites.add(site)
facebook.save()
