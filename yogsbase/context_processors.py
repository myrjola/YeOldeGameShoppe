from django.conf import settings


def base_variables(request):
    """Add variables used in the base templates."""
    return {'FACEBOOK_KEY': settings.SOCIAL_AUTH_FACEBOOK_KEY}
