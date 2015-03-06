from django.shortcuts import redirect
from django.views import generic
from django.core.urlresolvers import reverse, reverse_lazy
from django import http
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth import login as auth_login, authenticate
from oscar.apps.customer.views import RegisterUserMixin, EmailAuthenticationForm, EmailUserCreationForm
from . import signals



# ==========
# Shibboleth
# ==========

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from urllib import quote

LOGOUT_SESSION_KEY = getattr(settings, 'SHIBBOLETH_FORCE_REAUTH_SESSION_KEY', 'shib_force_reauth')

# Logout settings.


class ShibbolethView(TemplateView):
    """
    This is here to offer a Shib protected page that we can
    route users through to login.
    """
    template_name = 'shibboleth/user_info.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """
        Django docs say to decorate the dispatch method for
        class based views.
        https://docs.djangoproject.com/en/dev/topics/auth/
        """
        return super(ShibbolethView, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        """Process the request."""
        next = self.request.GET.get('next', None)
        if next is not None:
            return redirect(next)
        return super(ShibbolethView, self).get(request)

    def get_context_data(self, **kwargs):
        context = super(ShibbolethView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class ShibbolethLogoutView(TemplateView):
    """
    Pass the user to the Shibboleth logout page.
    Some code borrowed from:
    https://github.com/stefanfoulis/django-class-based-auth-views.
    """
    redirect_field_name = "next"

    def get(self, *args, **kwargs):
        #Log the user out.
        auth.logout(self.request)
        #Set session key that middleware will use to force
        #Shibboleth reauthentication.
        self.request.session[LOGOUT_SESSION_KEY] = True
        #Get target url in order of preference.
        target = settings.LOGOUT_REDIRECT_URL or \
                 quote(self.request.GET.get(self.redirect_field_name)) or \
                 quote(self.request.build_absolute_uri())
        logout = settings.SHIBBOLETH_LOGOUT_URL + '?target=%s' % target
        return redirect(logout)

class AccountAuthView(RegisterUserMixin, generic.TemplateView):
    """
    This is actually a slightly odd double form view that allows a customer to
    either login or register.
    """
    template_name = 'customer/login_registration.html'
    login_prefix, registration_prefix = 'login', 'registration'
    login_form_class = EmailAuthenticationForm
    registration_form_class = EmailUserCreationForm
    redirect_field_name = 'next'

    #Old login
    def get(self, request, *args, **kwargs):
        # If we come for a local login
        if 'local' in kwargs:
            if request.user.is_authenticated():
                return http.HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
            return super(AccountAuthView, self).get(
                request, *args, **kwargs)
        # If we want an SSO login
        else:
            # Remove session value that is forcing Shibboleth re-authentication.
            self.request.session.pop(LOGOUT_SESSION_KEY, None)
            next_target = self.request.GET.get(self.redirect_field_name)
            # No target defined redirects to the root page
            if next_target is None:
                next_target = '/'
            login = settings.SHIBBOLETH_LOGIN_URL + '?target=%s' % quote(next_target)
            if settings.DEBUG:
                print "Here I go again."
            user = authenticate(request_meta=self.request.META)
            if user is not None:
                auth_login(self.request, user)
            return redirect(login)


    def get_context_data(self, *args, **kwargs):
        ctx = super(AccountAuthView, self).get_context_data(*args, **kwargs)
        if 'login_form' not in kwargs:
            ctx['login_form'] = self.get_login_form()
        if 'registration_form' not in kwargs:
            ctx['registration_form'] = self.get_registration_form()
        return ctx

    def post(self, request, *args, **kwargs):
        # Use the name of the submit button to determine which form to validate
        if u'login_submit' in request.POST:
            return self.validate_login_form()
        elif u'registration_submit' in request.POST:
            return self.validate_registration_form()
        return http.HttpResponseBadRequest()

    # LOGIN

    def get_login_form(self, bind_data=False):
        return self.login_form_class(
            **self.get_login_form_kwargs(bind_data))

    def get_login_form_kwargs(self, bind_data=False):
        kwargs = {}
        kwargs['host'] = self.request.get_host()
        kwargs['prefix'] = self.login_prefix
        kwargs['initial'] = {
            'redirect_url': self.request.GET.get(self.redirect_field_name, ''),
        }
        if bind_data and self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def validate_login_form(self):
        form = self.get_login_form(bind_data=True)
        if form.is_valid():
            user = form.get_user()

            # Grab a reference to the session ID before logging in
            old_session_key = self.request.session.session_key

            auth_login(self.request, form.get_user())

            # Raise signal robustly (we don't want exceptions to crash the
            # request handling). We use a custom signal as we want to track the
            # session key before calling login (which cycles the session ID).
            signals.user_logged_in.send_robust(
                sender=self, request=self.request, user=user,
                old_session_key=old_session_key)

            msg = self.get_login_success_message(form)
            messages.success(self.request, msg)

            url = self.get_login_success_url(form)
            return http.HttpResponseRedirect(url)

        ctx = self.get_context_data(login_form=form)
        return self.render_to_response(ctx)

    def get_login_success_message(self, form):
        return _("Welcome back")

    def get_login_success_url(self, form):
        redirect_url = form.cleaned_data['redirect_url']
        if redirect_url:
            return redirect_url

        # Redirect staff members to dashboard as that's the most likely place
        # they'll want to visit if they're logging in.
        if self.request.user.is_staff:
            return reverse('dashboard:index')

        return settings.LOGIN_REDIRECT_URL

    # REGISTRATION

    def get_registration_form(self, bind_data=False):
        return self.registration_form_class(
            **self.get_registration_form_kwargs(bind_data))

    def get_registration_form_kwargs(self, bind_data=False):
        kwargs = {}
        kwargs['host'] = self.request.get_host()
        kwargs['prefix'] = self.registration_prefix
        kwargs['initial'] = {
            'redirect_url': self.request.GET.get(self.redirect_field_name, ''),
        }
        if bind_data and self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def validate_registration_form(self):
        form = self.get_registration_form(bind_data=True)
        if form.is_valid():
            self.register_user(form)

            msg = self.get_registration_success_message(form)
            messages.success(self.request, msg)

            url = self.get_registration_success_url(form)
            return http.HttpResponseRedirect(url)

        ctx = self.get_context_data(registration_form=form)
        return self.render_to_response(ctx)

    def get_registration_success_message(self, form):
        return _("Thanks for registering!")

    def get_registration_success_url(self, form):
        return settings.LOGIN_REDIRECT_URL
