class BaseContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for key in ["app", "page", "title"]:
            if hasattr(self, key):
                context[key] = getattr(self, key)
        return context
