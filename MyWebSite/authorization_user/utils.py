class AuthorizationUserMixin:
    def get_mixin_context(self, context: dict, **kwargs):
        context.update(kwargs)
        return context
