import calendar
from calendar import HTMLCalendar
from datetime import datetime

from django.views.generic import TemplateView

from .utils import HomeMixin


class HomeView(HomeMixin, TemplateView):
    template_name = 'main/home.html'

    @staticmethod
    def put_calendar(year: int = datetime.now().year, month: str = datetime.now().strftime('%B')):
        month = month.capitalize()
        month_number = list(calendar.month_name).index(month)
        month_number = int(month_number)
        return HTMLCalendar().formatmonth(year, month_number)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context=context, title='Home', calendar_object=self.put_calendar)
