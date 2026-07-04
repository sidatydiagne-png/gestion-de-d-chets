from django.views.generic import TemplateView


class LoginView(TemplateView):
    template_name = 'frontend/login.html'


class DashboardView(TemplateView):
    template_name = 'frontend/dashboard.html'


class CarteView(TemplateView):
    template_name = 'frontend/carte.html'


class SignalementsListView(TemplateView):
    template_name = 'frontend/signalements_list.html'


class SignalementCreateView(TemplateView):
    template_name = 'frontend/signalement_form.html'


class ZonesView(TemplateView):
    template_name = 'frontend/zones.html'


class CollectesView(TemplateView):
    template_name = 'frontend/collectes.html'
