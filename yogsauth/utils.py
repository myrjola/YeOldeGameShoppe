from django.core.mail import send_mail
from django.core.urlresolvers import reverse


def send_activation_email_to_user(user, request):
    """Send a link that will activate the user account."""
    activation_key = user.emailvalidation.activation_key
    activation_link = (request.get_host() +
                       reverse('activate',
                               kwargs={
                                   'user_id': user.id,
                                   'activation_key': activation_key
                               }))
    send_mail('Ye Olde Game Shoppe activation', activation_link,
              'yeoldegameshoppe', [user.email], fail_silently=False)
