from .utils import user_is_author


def author_group(request):
    return {
        'is_author': user_is_author(request.user),
    }
