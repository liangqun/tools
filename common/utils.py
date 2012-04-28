#encoding:utf-8

import cStringIO,urllib
from lxml import etree
import sys
import urllib2,cookielib
import re

def html2tree(data, encoding='utf-8'):
    parser = etree.HTMLParser(encoding=encoding)
    tree = etree.parse(cStringIO.StringIO(data), parser)
    return tree

def xml2tree(xmlfile):
    parser = etree.XMLParser(encoding='utf-8')
    tree = etree.parse(file(xmlfile), parser)
    return tree

    
from jinja2 import Template
def jinja_render_to_string(tmpl_file,c={}):
    return Template(file(tmpl_file).read().decode('utf8')).render(c)


cookie_jar = cookielib.LWPCookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
urllib2.install_opener(opener)
COOKIEFILE = 'r:/temp/cookies.lwp'

def get_or_post(theurl, postdata={}, txheaders={'User-agent' : 'Mozilla/4.0 (compatible; FireFox; Windows NT)'}):
    """
    theurl = 'http://www.ip138.com/ips8.asp'
    postdata = {
        'ip':ip,
        'action':'2'
    }
    data = get_or_post(theurl,postdata)
    """
    handle = None
    try:
        if postdata: 
            req = urllib2.Request(theurl, urllib.urlencode(postdata), txheaders)
        else:
            req = urllib2.Request(theurl, None, txheaders)
        handle = urllib2.urlopen(req)
    except IOError, e:
        print 'We failed to open "%s".' % theurl
        if hasattr(e, 'code'):
            print 'We failed with error code - %s.' % e.code
    
    
    cookie_jar.save(COOKIEFILE)
    return handle.read()

class MyDict(dict):
    """Example of overloading __getatr__ and __setattr__
    This example creates a dictionary where members can be accessed as attributes
    """
    def __init__(self, indict=None, attribute=None):
        if indict is None:
            indict = {}
        # set any attributes here - before initialisation
        # these remain as normal attributes
        self.attribute = attribute
        dict.__init__(self, indict)
        self.__initialised = True
        # after initialisation, setting attributes is the same as setting an item

    def __getattr__(self, item):
        """Maps values to attributes.
        Only called if there *isn't* an attribute with this name
        """
        try:
            return self.__getitem__(item)
        except KeyError:
            raise AttributeError(item)

    def __setattr__(self, item, value):
        """Maps attributes to values.
        Only if we are initialised
        """
        if not self.__dict__.has_key('_attrExample__initialised'):  # this test allows attributes to be set in the __init__ method
            return dict.__setattr__(self, item, value)
        elif self.__dict__.has_key(item):       # any normal attributes are handled normally
            dict.__setattr__(self, item, value)
        else:
            self.__setitem__(item, value)

def to_unicode(text):
    if isinstance(text,unicode):
        return text
    text = str(text)
    try:
        return text.decode('utf-8')
    except UnicodeError:
        try:
            return text.decode('gb18030')
        except UnicodeError:
            return u'UnicodeError'

def to_gbk(text):
    if text is None:
        return None
    elif isinstance(text,unicode):
        return text.encode('gb18030')
    else:
        try:
            return text.decode('utf-8').encode('gb18030')
        except UnicodeError:
            return text

def to_utf8(text):
    if isinstance(text,unicode):
        return text.encode('utf-8')
    else:
        try:
            text.decode('utf-8') #这里是通过解码来检查是否是utf-8编码，不能直接返回解码后的内容，只能返回解码前的内容！
            return text            
        except UnicodeError:
            pass
        
        try:
            return text.decode('gb18030').encode('utf-8')
        except UnicodeError:
            return 'UnicodeError'


def my_input(msg):
    return raw_input(to_gbk(msg))


def confirm_or_exit(msg):
    if not 'y' == my_input(msg):
        sys.exit()

def console_select(datalist, title, prompt):
    if title[-1] == ':':
        print title
    else:
        print title+":"
    i = 0
    for data in datalist:
        i+=1
        print u'%d - %s' % (i,data)
    select = my_input('%s: ' % prompt)
    if select in ['x','q','exit','quit']:
        print 'User canceled.'
        sys.exit(0)
    if select.isdigit():
        select = int(select)
        if select>0 and select<=len(datalist):
            data = datalist[select-1]
            return data
        else:
            print 'Warning! Please give a number between 1 and %d!' % len(datalist)
            print
            return console_select(datalist, title, prompt)
    else:
        print 'Warning! Please give a number between 1 and %d!' % len(datalist)
        print
        return console_select(datalist, title, prompt)


import txt2tags
t2t_config = txt2tags.ConfigMaster()._get_defaults()
t2t_config['target'] = 'html'   # formato de saida: HTML
#t2t_config['postproc'] = [('@@','<BR>')]

def t2t(text):
    if not text:
        return ''
    if isinstance(text,unicode):
        text = text.encode('utf8')
    texto = text.split('\n')   # deve ser uma lista
    result, toc = txt2tags.convert(texto, t2t_config)
    #~ result, toc = txt2tags.convert(texto, t2t_config)

    return re.sub('@@','<br>','\n'.join(result)).decode('utf8')     # result eh uma lista