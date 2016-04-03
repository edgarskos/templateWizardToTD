# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import pywikibot
import json
from pywikibot import pagegenerators
from collections import OrderedDict

site = pywikibot.getSite()
categoryName = 'קטגוריה:תבניות_הנתמכות_על_ידי_אשף_התבניות'

cat = pywikibot.Category(pywikibot.Link(categoryName,defaultNamespace=14))
defaultParam='ברירת מחדל'
for template in cat.articles():
    orgText = template.get()
    if re.findall('templatedata',orgText):
        print('%s already have tempaltedata'%template.title())
        continue
    templateData = OrderedDict()
    templateParams=OrderedDict()
    paramsPage = pywikibot.Page(site,template.title()+'/פרמטרים')
    paramsText = ''
    try:
        paramsText = paramsPage.get()
    except pywikibot.NoPage:
        template.put(orgText.replace('{{אשף תבניות}}',''),'לא קיים דף פרמטרים')
        continue

    description=None
    for line in paramsText.splitlines():
        if re.match('\|[-\}]\s*',line):
            continue
        if re.findall('tpw_globalExplanation',line):
            templateData['description'] = re.sub('!.*?\|','',line)
        if line[0]=='|':
            paramData = line.split('||')
            paramName = paramData[0][1:]#.strip()?
            
            paramDesc = paramData[1].strip()
            paramDesc = re.sub('</?nowiki>','',paramDesc)
            
            paramProp = paramData[2] if len(paramData)>2 else ''
            templateParams[paramName] = OrderedDict({
                'description': paramDesc
            })
            
            for prop in paramProp.split(';'):
                prop=prop.strip()
                m = re.match('\s*ברירת מחדל\s*=(.+)',prop)
                if m:
                    templateParams[paramName]['default'] = m.group(1)
                m = re.match('\s*שדה חובה',prop)
                if m:
                    templateParams[paramName]['required'] = True;

    templateData['params']=templateParams
    newText = '<noinclude><br clear="both"><templatedata>%s</templatedata></noinclude>'%json.dumps(templateData,ensure_ascii=False,indent=4)
    template.put(orgText+newText, 'הוספת templatedata עפי דף הפרמטרים')
    break
print('finished')
