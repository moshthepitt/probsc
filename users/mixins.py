from django.http import Http404


class BelongsToUserMixin(object):
    """
    Ensure the object belongs to current user
    """

    def dispatch(self, *args, **kwargs):
        if self.get_object().user != self.request.user:
            raise Http404
        return super(BelongsToUserMixin, self).dispatch(*args, **kwargs)
