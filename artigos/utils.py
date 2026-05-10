GROUP_NAME = 'autores'


def user_is_author(user):
    return (
        user.is_authenticated
        and user.groups.filter(name=GROUP_NAME).exists()
    )
