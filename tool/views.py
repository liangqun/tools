#encoding=utf8

from common.render_decorator import render_to
from calenda_utils import make_calenda
import os
import re
import datetime
import settings
from django.shortcuts import HttpResponseRedirect,Http404,HttpResponse
script_path = os.path.dirname(os.path.abspath(__file__))

@render_to('tool/index.html')
def index(request):
    return locals()

@render_to('tool/calenda_maker.html')
def calenda_maker(request):
    if request.method == 'POST':
        tasks = request.POST.get('tasks','')
        task_list = re.split(r'[\r\n]+',tasks)
        if not task_list:
            errmsg = u'请输入任务列表'
        try:
            days = int(request.POST.get('days',30))
        except ValueError:
            days = 30
        date_from = datetime.datetime.now()
        tmp_dir = settings.FILE_ROOT
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)
        save_as = os.path.join(tmp_dir,'calenda.xlsx')
        make_calenda(task_list, date_from, days, save_as)
        #download_link = '/static/file/calenda.xls'

        data = open(save_as,'rb').read()
        response = HttpResponse(data,mimetype='application/octet-stream')
        response['Content-Disposition'] = (u'attachment; filename=%s' % os.path.basename('calenda.xlsx'))
        return response

    #params = app.__dict__
    #params1 = sae.__dict__
    #params2 = sae.core.__dict__
    return locals()

