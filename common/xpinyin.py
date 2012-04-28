#!/usr/bin/env python
# encoding: utf-8
"""
Translate chinese hanzi to pinyin by python
Created by Eric Lo on 2010-05-20.
Copyright (c) 2010 __lxneng@gmail.com__. http://lxneng.com All rights reserved.
"""

import os

class Pinyin(object):
    
    script_path = os.path.split(os.path.realpath(__file__))[0]
    
    def __init__(self, data_path=os.path.join(script_path,'Mandarin.dat')):
        self.dict = {}
        for line in open(data_path):
            k, v = line.split('\t')
            self.dict[k] = v
    
    def get_pinyin(self, chars=u"你好吗"):
        if not isinstance(chars, unicode):
            try:
                chars = chars.decode('utf-8')
            except UnicodeDecodeError:
                chars = chars.decode('gb18030')
        result = []
        for char in chars:
            key = "%X" % ord(char)
            
            try:
                result.append(self.dict[key].split(" ")[0].strip()[:-1])
            except:
                result.append(char)
        return ''.join(result)

    def get_initials(self, char=u'你'):
        try:
            return self.dict["%X" % ord(char)].split(" ")[0][0]
        except:
            return char
            
    def get_pinyin_name(self, chars=u"张三在"):
        if not chars:
            return chars
        pinyin1 = self.get_pinyin(chars[0]).capitalize()
        
        pinyin2 = ''
        if len(chars)>1:
            pinyin2 = self.get_pinyin(chars[1:]).capitalize()
        
        return ' '.join((pinyin1,pinyin2))
    
    def get_pinyin_diqu(self, chars=u"北方的的"):
        return self.get_pinyin(chars).capitalize().replace('rbo',' RBO')

if __name__ =="__main__":
    t = Pinyin()
    print t.get_pinyin(u'RBO')
    print t.get_pinyin_diqu(u'北京RBO')
    print t.get_pinyin_name(u'张三')