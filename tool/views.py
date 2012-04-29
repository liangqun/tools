#encoding=utf8

from common.render_decorator import render_to
from calenda_utils import make_calenda
import os
import re
import datetime
import time
import settings
from django.shortcuts import HttpResponseRedirect,Http404,HttpResponse

from common.log_utils import getLogger
log = getLogger('tool.views')

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

        date_from_str = request.POST.get('date_from')
        date_from = time.strptime(date_from_str, "%Y-%m-%d")
        date_from = datetime.datetime(*date_from[0:5])
        ttype = request.POST.get('ttype')
        if ttype == '1':
            date_to_str = request.POST.get('date_to')
            date_to = time.strptime(date_to_str, "%Y-%m-%d")
            date_to = datetime.datetime(*date_to[0:5])
            delta = date_to - date_from
            days = delta.days
        elif ttype == '2':
            days_str = request.POST.get('days')
            days = int(days_str)

        tmp_dir = settings.FILE_ROOT
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)
        save_as = os.path.join(tmp_dir,'calenda.xlsx')
        log.debug('date_from=%s' % date_from)
        log.debug('days=%s' % days)
        make_calenda(task_list, date_from, days, save_as)
        #download_link = '/static/file/calenda.xls'

        data = open(save_as,'rb').read()
        response = HttpResponse(data,mimetype='application/octet-stream')
        response['Content-Disposition'] = (u'attachment; filename=%s' % os.path.basename('calenda.xlsx'))
        return response

    return locals()

