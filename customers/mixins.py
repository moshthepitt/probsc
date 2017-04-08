from django.http import Http404


class CustomerFormMixin(object):
    """
    Used in form views for forms that need an initial customer
    """

    def get_initial(self):
        initial = super(CustomerFormMixin, self).get_initial()
        initial['customer'] = self.request.user.userprofile.customer
        return initial


class CustomerCheckMixin(object):
    """
    Used in detail and update views to ensure that the user has the right to view the object
    """
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            # if current user is not tied to a customer then redirect them away
            if not self.request.user.userprofile.customer:
                raise Http404
            # if current user is not tied to a subscription then redirect them away
            if self.request.user.userprofile.customer != self.get_object().customer:
                raise Http404
        return super(CustomerCheckMixin, self).dispatch(*args, **kwargs)


class CustomerExistsMixin(object):
    """
    Used to make sure the user has a valid customer
    """
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            if not self.request.user.userprofile.customer:
                raise Http404
        return super(CustomerExistsMixin, self).dispatch(*args, **kwargs)


class CustomerFilterMixin(object):
    """
    Modifies the Queryset to flter items by current customer
    """

    def get_queryset(self):
        queryset = super(CustomerFilterMixin, self).get_queryset()
        return queryset.filter(customer=self.request.user.userprofile.customer)
