#encoding:utf-8
import cStringIO,urllib
from lxml import etree

def html2tree(url):
    html = urllib.urlopen(url).read()
    parser = etree.HTMLParser(encoding='utf-8')
    tree = etree.parse(cStringIO.StringIO(html), parser)
    return tree,html

def xml2tree(xmlfile):
    parser = etree.XMLParser(encoding='utf-8')
    tree = etree.parse(file(xmlfile), parser)
    return tree