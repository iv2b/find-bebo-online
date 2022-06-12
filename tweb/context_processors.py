from django.shortcuts import get_object_or_404

from tweb.models import CustomUser


def userContext(request):
    try:
        CU = CustomUser.objects.get(pk = request.user.id)
    except:
        CU = None
    return {'CustomUserContext': CU}