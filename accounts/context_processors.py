from .utils import user_is_portfolio_manager


def portfolio_manager(request):
    return {
        'is_portfolio_manager': user_is_portfolio_manager(request.user),
    }
