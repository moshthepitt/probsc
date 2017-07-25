from django.http import Http404


class BelongsToUserMixin(object):

    def dispatch(self, *args, **kwargs):
        if self.get_object().user != self.request.user:
            raise Http404
        return super(BelongsToUserMixin, self).dispatch(*args, **kwargs)
