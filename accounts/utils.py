GROUP_NAME = 'gestor-portfolio'


def user_is_portfolio_manager(user):
    return (
        user.is_authenticated
        and user.groups.filter(name=GROUP_NAME).exists()
    )
