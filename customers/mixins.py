

class CustomerFormMixin(object):
    """
    Used in form views for forms that need an initial customer
    """

    def get_initial(self):
        initial = super(CustomerFormMixin, self).get_initial()
        initial['customer'] = self.request.user.userprofile.customer
        return initial
