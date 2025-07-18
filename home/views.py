from django.shortcuts import render
from django.views.generic import TemplateView,ListView
from product.models import Product,Job
from . models import SiteStatistics
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.utils.timezone import now

class Home(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve all products
        products = Product.objects.all()
        jobs=Job.objects.all()
        # Add products to context
        self.request.session.get('my_name','ali')

        # start view site---------------------------------------------------------------------------
        stats, created = SiteStatistics.objects.get_or_create(id=1)
        today = now().date()
        week_start = (now() - timedelta(days=now().weekday())).date()
        stats.total += 1
        # Check if last_visit_date is today
        if stats.last_visit_date != today:
            # Reset daily count if day has changed
            stats.daily_visits = 1
            stats.last_visit_date = today
        else:
            stats.daily_visits += 1

        # Check if last visit was in the current week
        if stats.last_week_start != week_start:
            # Reset weekly count if week has changed
            stats.weekly_visits = 1
            stats.last_week_start = week_start
        else:
            stats.weekly_visits += 1
        stats.save()  
        # Add stats to context
        context['visit_count'] = stats
        context['daily_visits'] = stats.daily_visits
        context['weekly_visits'] = stats.weekly_visits
        # end view site-----------------------------------------------------------------------------

        context['products'] = products
        context['jobs'] = jobs
        return context    

def aboutus(request):
    return render(request,'home/aboutus.html',{})

def jobdetail(request,id):
    jobs = Job.objects.get(id=id)
    return render(request,'product/job.html', context={'jobs':jobs})       



