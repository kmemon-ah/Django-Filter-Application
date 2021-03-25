from .models import *
from django.shortcuts import render
from datetime import datetime, timedelta


def index(request):
    keys = []
    usr = []
    usd = []
    sfrom = []
    via = []
    dates = []
    all_key = []
    occurance = []

    keywords = Keyword_Data.objects.all().order_by('-search_time')

    for k in keywords:
        all_key.append(k.keyword)

        if k.keyword not in keys:
            keys.append(k.keyword)
            
        if k.user not in usr:
            usr.append(k.user)
            
        if k.used not in usd:
            usd.append(k.used)

        if k.searched_from not in sfrom:
            sfrom.append(k.searched_from)

        if k.searched_via not in via:
            via.append(k.searched_via)

        if k.search_time.date() not in dates:
            dates.append(k.search_time.date())
        
    for k in keys:
        count = all_key.count(k)
        occurance.append(count)
    
    zipped = zip(keys,occurance)
    d = dict(list(zipped))
    final_key = dict(sorted(d.items(), key=lambda item: item[1], reverse=True))

    usr.sort()

    context = {
        'keywords':keywords,
        'keys':keys,
        'user':usr,
        'used':usd,
        'location':sfrom,
        'device':via,
        'dates':dates,
        'zipped':zipped,
        'final_key':final_key
    }

    if request.method == 'POST':
        keys = []
        usr = []
        usd = []
        sfrom = []
        via = []
        dates = []

        keywords = Keyword_Data.objects.all().order_by('-search_time')

        for k in keywords:
            if k.keyword not in keys:
                keys.append(k.keyword)

            if k.user not in usr:
                usr.append(k.user)
                
            if k.used not in usd:
                usd.append(k.used)

            if k.searched_from not in sfrom:
                sfrom.append(k.searched_from)

            if k.searched_via not in via:
                via.append(k.searched_via)

            if k.search_time.date() not in dates:
                dates.append(k.search_time.date())

        for k in keys:
            count = all_key.count(k)
            occurance.append(count)
        

        zipped = zip(keys,occurance)
        d = dict(list(zipped))
        final_key = dict(sorted(d.items(), key=lambda item: item[1], reverse=True))
        

        usr.sort()
        
        key = request.POST.getlist('keys')
        user = request.POST.getlist('user')
        time = request.POST.get('time')
        used = request.POST.getlist('used')
        location = request.POST.getlist('location')
        dv = request.POST.getlist('dv')

        if len(key)<1:
            key = []
            for k in keywords:
                key.append(k.keyword)

        if len(user)<1:
            user = []
            for k in keywords:
                user.append(k.user)

        if len(used)<1:
            used = []
            for k in keywords:
                used.append(k.used)

        if len(location)<1:
            location = []
            for k in keywords:
                location.append(k.searched_from)

        if len(dv)<1:
            dv = []
            for k in keywords:
                dv.append(k.searched_via)

        keywords = Keyword_Data.objects.filter(keyword__in=key, user__in=user, used__in=used, searched_from__in = location, searched_via__in = dv)

        if time == 'Yesterday':
            yesterday = datetime.today() - timedelta(days=1)
            keywords = Keyword_Data.objects.filter(keyword__in=key, user__in=user, used__in=used, searched_from__in = location, searched_via__in = dv, search_time__gte = yesterday)
        
        if time == 'Week':
            week = datetime.today() - timedelta(days=7)
            keywords = Keyword_Data.objects.filter(keyword__in=key, user__in=user, used__in=used, searched_from__in = location, searched_via__in = dv, search_time__gte = week)
        
        if time == 'Month':
            # month = datetime.today() -  timedelta(weeks=4)
            year = datetime.today().year
            month = datetime.today().month
            month = int(month) - 1
            m = f'{year}-{month}-01 00:00:00.000000'
            keywords = Keyword_Data.objects.filter(keyword__in=key, user__in=user, used__in=used, searched_from__in = location, searched_via__in = dv, search_time__gte = m)


        context = {
            'keywords':keywords,
            'keys':keys,
            'user':usr,
            'used':usd,
            'location':sfrom,
            'device':via,
            'dates':dates,
            'zipped':zipped,
            'final_key':final_key
        } 

        return render(request, 'index.htm',context)

    return render(request, 'index.htm',context)
