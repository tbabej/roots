# Bootstraps the Roots instance with the default
# set of the necessary objects

import datetime

site = Site.objects.get_current()

# Create the admin user
admin = User.objects.create(
    username="admin",
    email="admin@example.com",
    is_staff=True,
    is_superuser=True,
)
admin.set_password('admin')
admin.save()

# Add his email to allauth table as verified and primary
email = EmailAddress.objects.create(
    user=admin,
    email="admin@example.com",
    verified=True,
    primary=True
)

# Create sample address and school for admin
address = Address.objects.create(
    street="Street1",
    city="City1",
    postal_number="10001",
    region="Region1"
)

school = School.objects.create(
    name="Sample School",
    address=address,
    abbreviation="SmpSch"
)

userprofile = admin.userprofile
userprofile.school = school
userprofile.school_class = "Z9"
userprofile.classlevel = "Z9"
userprofile.save()

# Add competition with sample severity, category
# with 1 season composed of 1 series
# with its corresponding problem set of 1 problem
competition = Competition.objects.create(
    name="Sample competition",
    site=site
)

severity = ProblemSeverity.objects.create(
    name="Sample Severity",
    level=1,
    competition=competition
)

category = ProblemCategory.objects.create(
    name="Sample Category",
    competition=competition
)

problem = Problem.objects.create(
    text="Given numbers 5 and 6, calculate their sum.",
    result="11",
    severity=severity,
    category=category,
    competition=competition
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

probleminset = ProblemInSet.objects.create(
    problem=problem,
    problemset=problemset_series_1,
    position=0
)

series = Series.objects.create(
   season=season,
   name="First series",
   number=1,
   submission_deadline=datetime.datetime.now()+datetime.timedelta(days=30),
   problemset=problemset_series_1
)

# Create admin's solution for the problem
usersolution = UserSolution.objects.create(
    user=admin,
    problem=problem,
    score=9
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
