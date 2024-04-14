
from django.http import Http404

def check_user_able_to_see_page(*groups):

    def decorator(function):
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name__in=groups).exists() or 'Todos' in groups:
                return function(request, *args, **kwargs)
            else:
                raise Http404

        return wrapper

    return decorator