from django.conf import settings


def global_settings(request):
    # return any necessary values
    return {
        'APP_NAME': 'Quora',

    }
