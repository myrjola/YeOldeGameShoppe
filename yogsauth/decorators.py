from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse_lazy

from yeoldegameshoppe.utils import lazy_format


def _user_group_required(function=None, user_group=''):
    """Decorator for views that checks that the user is in a certain user group.

    It also checks that the user is logged in and if the test is not passed it
    redirects back to the profile page.
    """
    # Redirect back to profile. We use a query parameter to show a message.
    redirect_url = lazy_format("{}?{}_activation_needed=1",
                               reverse_lazy('profile'), user_group)

    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated() and hasattr(u, user_group),
        login_url=redirect_url)
    if function:
        return actual_decorator(function)
    return actual_decorator


def developer_required(function=None):
    """Decorator for views that checks that the user is a Developer."""
    return _user_group_required(function, user_group='developer')


def player_required(function=None):
    """Decorator for views that checks that the user is a Player."""
    return _user_group_required(function, user_group='player')
