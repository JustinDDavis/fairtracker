from django.contrib.auth.models import User
from fair.models import Fair


def get_dummy_user(username='testuser'):
    return User.objects.get_or_create(username=username)[0]


def create_fair(name="Fair 1"):
    fair = standard_fair(name)
    fair.save()
    return fair

def get_fair(id):
    return Fair.objects.get(pk=id)

def standard_fair(name="Fair"):
    return Fair.objects.create(name=f"Test {name}",
                               city=f"Test {name}",
                               state=f"Test {name}",
                               owner=get_dummy_user())