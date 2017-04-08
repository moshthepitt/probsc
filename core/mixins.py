from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_protect

from .forms import ListViewSearchForm
from .decorators import cache_page_on_auth, cache_page_for_user


class CSRFMixin(object):
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(CSRFMixin, self).dispatch(*args, **kwargs)


class CachePageMixin(object):
    @method_decorator(cache_page(60 * 30))
    def dispatch(self, *args, **kwargs):
        return super(CachePageMixin, self).dispatch(*args, **kwargs)


class CachePageOnAuthMixin(object):
    @method_decorator(cache_page_on_auth(60 * 30))
    def dispatch(self, *args, **kwargs):
        return super(CachePageOnAuthMixin, self).dispatch(*args, **kwargs)


class CachePageForUserMixin(object):
    @method_decorator(cache_page_for_user(60 * 30))
    def dispatch(self, *args, **kwargs):
        return super(CachePageForUserMixin, self).dispatch(*args, **kwargs)


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class StaffmemberRequiredMixin(object):
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffmemberRequiredMixin, self).dispatch(request, *args, **kwargs)


class CoreFormMixin(object):
    """
    Adds some nice stuff to formviews used in create/update views
    """

    def get_form_kwargs(self):
        kwargs = super(CoreFormMixin, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        return self.object.get_edit_url()


class ListViewSearchMixin(object):
    """
    Adds search to listview
    """
    form_class = ListViewSearchForm

    def get_queryset(self):
        queryset = super(ListViewSearchMixin, self).get_queryset()
        form = self.form_class(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data['name'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListViewSearchMixin, self).get_context_data(**kwargs)
        form = self.form_class()
        if self.request.GET.get('name'):
            form = self.form_class(initial={'name': self.request.GET.get('name')})
        context['form'] = form
        return context


class VerboseNameMixin(object):
    """
    Sets the Model verbose name in the context data
    Used in Generic CRUD views
    """

    def get_context_data(self, **kwargs):
        context = super(VerboseNameMixin, self).get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name
        context['verbose_name_plural'] = self.model._meta.verbose_name_plural
        return context
