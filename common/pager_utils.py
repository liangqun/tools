
import urllib
from django.core.paginator import Paginator, InvalidPage

def get_page_list(total_page,current_page):
    current_page = int(current_page)
    if total_page <= 10:
        return [range(1,total_page+1)]


    set_begin = set()
    set_middle = set()
    set_end = set()

    set_begin.add(1)
    set_begin.add(2)

    set_middle.add(current_page-2)
    set_middle.add(current_page-1)
    set_middle.add(current_page)
    set_middle.add(current_page+1)
    set_middle.add(current_page+2)

    set_end.add(total_page-1)
    set_end.add(total_page)

    list1=list(set_begin)
    list1.sort()

    list2=list(set_middle)
    list2.sort()

    list3=list(set_end)
    list3.sort()

    if list2[0] < list1[-1]+2 :
        set_begin.update(set_middle)
        set_middle = None
    elif list2[-1] > (list3[0]-2) :
        set_end.update(set_middle)
        set_middle = None
    output = []
    list_begin = [i for i in list(set_begin) if i > 0]
    list_end = [i for i in list(set_end) if i <= total_page]

    list_begin.sort()
    list_end.sort()

    output.append(list_begin)
    if set_middle:
        list_middle = list(set_middle)
        list_middle.sort()
        output.append(list_middle)
    output.append(list_end)

    return output

def _get_page_url(pager,current_page,params=None):
    old_params = '?'
    page_name = 'page'
    if params:
        try:
            page_name = params.pop('page_name')
        except KeyError:
            pass    
        for key in params:
            #old_params += '%s=%s&' % (key,params[key])
            old_params = '%s%s&' % (old_params,urllib.urlencode({key:unicode(params[key]).encode('utf-8')}))
    current_page = int(current_page)
    page_list = get_page_list(pager.page_range[-1],current_page)
    
    output = ['<div class="pageframe"><div class="pagebox" id="_function_code_page" align="right"><table><tr>']
    
    loop = 0    
    for list in page_list:
        loop += 1
        for i in list:
            if i == current_page:
                output.append('<td><div class="pagebox_num_nonce" >%d</div></td>' % (i))
            else:
                output.append('<td><div class="pagebox_num" ><a href="%s%s=%d">%d</a></div></td>' % (old_params,page_name,i,i))
        if loop < len(page_list):
            output.append('<td><div class="pagebox_block" >...</div></td>')
    output.append('</tr></table></div></div>')
    return '\n'.join(output)

class Pager(object):
  def __init__(self,request,obj_list,page_size=10,page_name='page',params=None):
    try:
        pager = Paginator(obj_list,page_size)
        try:
            self.current_page = int(request.GET.get(page_name) or 1)
        except AttributeError:
            self.current_page = int(request.args.get(page_name) or 1)
    except InvalidPage: 
        return ([],'')
    
    if self.current_page < 1: self.current_page = 1
    if self.current_page > pager.num_pages: self.current_page = pager.num_pages

    self.obj_list = pager.page(self.current_page).object_list
    self.num_pages = pager.num_pages
    
    if self.num_pages == 1:
        self.page_url = ''
    else:
        self.page_url = _get_page_url(pager,self.current_page,params)
  