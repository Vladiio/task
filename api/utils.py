from rest_framework import exceptions


def fetch_token(request, model):
    token_header = request.META.get('HTTP_AUTHORIZATION')

    if not token_header:
        raise exceptions.AuthenticationFailed('Token was not provided')

    try:
        key = token_header.split(' ')[1]
        token = model.objects.get(key=key)
    except IndexError:
        raise exceptions.AuthenticationFailed('Invalid token header')
    except model.DoesNotExist:
        raise exceptions.AuthenticationFailed('Invalid token')
