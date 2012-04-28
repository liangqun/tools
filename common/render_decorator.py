#encoding=utf-8
from django.http import HttpResponse,HttpResponseRedirect
from common.decorator import decorator
from common.json_utils import obj_to_json_for_ajax
from django.shortcuts import render_to_response
from django.template import RequestContext

def render_to(template):
    """
    Decorator for Django views that sends returned dict to render_to_response function.

    Template name can be decorator parameter or TEMPLATE item in returned dictionary.
    RequestContext always added as context instance.
    If view doesn't return dict then decorator simply returns output.

    Parameters:
     - template: template name to use

    Examples:
    # 1. Template name in decorator parameters

    @render_to('template.html')
    def foo(request):
        bar = Bar.object.all()  
        return {'bar': bar}

    # equals to 
    def foo(request):
        bar = Bar.object.all()  
        return render_to_response('template.html', 
                                  {'bar': bar}, 
                                  context_instance=RequestContext(request))

    # 2. Template name as TEMPLATE item value in return dictionary

    @render_to()
    def foo(request, category):
        template_name = '%s.html' % category
        return {'bar': bar, 'TEMPLATE': template_name}
    
    #equals to
    def foo(request, category):
        template_name = '%s.html' % category
        return render_to_response(template_name, 
                                  {'bar': bar}, 
                                  context_instance=RequestContext(request))
    """

    def renderer(function):
        def wrapper(request, *args, **kwargs):
            output = function(request, *args, **kwargs)
            if not isinstance(output, dict):
                return output
            tmpl = output.pop('TEMPLATE', template)
            return render_to_response(tmpl, output, context_instance=RequestContext(request))
        return wrapper
    return renderer

@decorator
def render_to_ajax(func, *args, **kw):
    output = func(*args, **kw)
    if not isinstance(output, tuple):
        return HttpResponse('bad view. ajax view must return a tuple object and tuple[0] is True or False')
    if not isinstance(output[0],bool):
        return HttpResponse('bad view. ajax view must return a tuple object and tuple[0] is True or False')
    
    return HttpResponse(obj_to_json_for_ajax(output))
