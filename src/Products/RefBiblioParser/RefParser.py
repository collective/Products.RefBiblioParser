# -*- coding: utf-8 -*-
##########################################################################
#                                                                        #
#              copyright (c) 2004 Belgian Science Policy                 #
#                                 and contributors                       #
#                                                                        #
#    maintainers: David Convent, david.convent_AT_naturalsciences.be     #
#                 Louis Wannijn, louis.wannijn_AT_naturalsciences.be     #
#                                                                        #
##########################################################################

""" A parser for CMFBibliographyAT that knows about the Ref format
"""

# Python stuff
import re, sys

# Zope stuff
from Globals import InitializeClass
from App.Dialogs import MessageDialog

from zope.interface import implements

# Bibliography stuff
from bibliograph.parsing.parsers.base import BibliographyParser


class RefParser(BibliographyParser):
    """ specific parser to process input in Ref-format
    """

    meta_type = "Ref Parser"
    available = True
    file_extension = 'REF'
    format = {'name':'Ref',
              'extension':'REF'}

    def __init__(self,
                 id = 'ref',
                 title = "Ref parser",
                 delimiter = '\r?\n\r?\n',
                 pattern = '^(%[A-Z]) ([^\n\r]*)'):
        """
        initializes including the regular expression patterns
        """
        self.id = id
        self.title = title
        self.setDelimiter(delimiter)
        self.setPattern(pattern, re.M)
    # Here we need to provide 'checkFormat' and 'parseEntry'

    # rewrite
    def checkFormat(self, source):
        """
        is this my format?
        """
        teststring = source[:200].lower()
        ai = teststring.find('%T')
        ei = teststring.find('%A')
        di = teststring.find('%D')
        if ai + ei + di > -2:
            return 1
        else:
            return 0

    def preprocess(self, source):
        """
        replaces richtext formatting with html tags
        """
        #source = unicode(source,'iso-8859-1').encode('utf-8')
        return self.convertRichToHtml(source)

    def convertRichToHtml(self, source):
        richformat = re.compile(r'\{\\(\w+) ([^{}\n]+)}')
        iterator = richformat.finditer(source)
        for match in iterator:
           newstring='<%s> %s </%s>' % (match.group(1), match.group(2), match.group(1))
           #start=match.start()
           #stop=match.end()
           source.replace(match.group(0),newstring)
        return source

    # done with preprocessing

    def parseEntry(self, entry):
        """
        parses a single entry
        
        returns a dictionary to be passed to
        BibliographyEntry's edit method
        """
        result = {}
        
        tokens = self.pattern.finditer(entry)

        # some defaults
        result['note'] = 'automatic ref import'
        for line in tokens:
          try:
        
            key=line.group(1)
            value=line.group(2)
            if key == '%A':
                
                value=value.replace('.-','-dot-')
                value=value.replace('.','. ')
                value=value.replace('-dot','.-')
                
                lastauthor=''
                if ' & ' in value:
                    lastauthor = value.split(' & ',2)[-1]
                    value = value.split(' & ',2)[0]
                if ' et ' in value.lower(): 
                    lastauthor = value.split(' et ',2)[-1]
                    value = value.split(' et ',2)[0]
                if ' en ' in value.lower(): 
                    lastauthor = value.split(' en ',2)[-1]
                    value = value.split(' en ',2)[0]
                authlist= value.split(',')
                if not lastauthor == '':
                    authlist.append(lastauthor)
                    
                for auth in authlist:
                    raw = auth.strip().split(' ',3)
                    if raw[0].lower() in ['van', 'von', 'du', 'de'] and len(raw)>1: 
                         raw[0] = raw[0]+' '+raw[1]
                         raw.pop(1)
                    lname = raw[0].strip()
                    fname = ''
                    mname = ''
                    if len(raw)>1: fname = raw[1].strip()
                    if len(raw)>2: mname = raw[2].strip()
                    adict = {'firstname': fname
                             ,'middlename': mname
                             ,'lastname': lname
                             }
                    result.setdefault('authors',[]).append(adict)
            elif key == '%B': 
                result['booktitle'] = str(value).strip()
                for i in ['acte', 'proceedings', 'akte']:
                    if i in str(value).strip().lower(): result['publication_type'] = 'InproceedingsReference'
                if not result.has_key('publication_type'): result['publication_type'] = 'InbookReference'
            elif key == '%C': result['city'] = str(value).strip()
            elif key == '%D': 
                date = str(value).strip().lower()
                if date == 'in press':
                    if result.has_key('note'): 
                        result['note'] += "\n %s" % str(value).strip()
                    else: 
                        result['note'] += "\n %s" % str(value).strip()
                elif not (date in ['n. d.','s. d.']):
                    result['publication_year'] = str(value).strip()
            elif key == '%E': 
                if not result.has_key('editor'):
                    result['editor'] = str(value).strip()
                else:
                    result['editor'] += ', %s' % str(value).strip()
            elif key == '%I': result['publisher'] = str(value).strip()
            elif key == '%J': 
                result['journal'] = str(value).strip()
                result['publication_type'] = 'ArticleReference'
            elif key == '%K': 
                if result.has_key('subject'): 
                    result['subject'] += '\n' + '\n'.join([key.strip() for key in str(value).split(',')])
                else:
                    result['subject'] = '\n'.join([key.strip() for key in str(value).split(',')])
            elif key == '%N': result['number'] = str(value).strip()
            elif key == '%O': 
                if result.has_key('abstract'):
                    result['abstract'] += "\n %s" % str(value).strip()
                else:
                    result['abstract'] = "%s" % str(value).strip()
            elif key == '%P': result['pages'] = str(value).strip()
            elif key == '%R': 
                for i in ['acte', 'proceedings', 'akte']:
                    if i in str(value).strip().lower(): 
                        result['publication_type'] = 'ProceedingsReference'
                        if result.has_key('note'):
                            result['note'] += "\n %s" % str(value).strip()
                        else:
                            result['note'] = "%s" % str(value).strip()
                for i in ['thesis', 'eindwerk', 'thèse']:
                    if i in str(value).strip().lower(): 
                        result['publication_type'] = 'MastersthesisReference'
                        if result.has_key('note'):
                            result['note'] += "\n %s" % str(value).strip()
                        else:
                            result['note'] = "%s" % str(value).strip()
                for i in ['raport', 'report', 'verslag']:
                    if i in str(value).strip().lower(): 
                        result['publication_type'] = 'TechreportReference'
                        result['type'] = str(value).strip()
                if not result.has_key('publication_type'): 
                        result['publication_type'] = 'BookReference'
                        if result.has_key('note'):
                            result['note'] += "\n %s" % str(value).strip()
                        else:
                            result['note'] = "%s" % str(value).strip()
            elif key == '%T': result['title'] = str(value).strip()
            elif key == '%V': result['volume'] = str(value).strip()
            elif key == '%X': 
                if result.has_key('note'):
                    result['note'] += "\n %s" % str(value).strip()
                else:
                    result['note'] = "%s" % str(value).strip()
          except:
            result['upload_status'] = "Error type: %s.\nError value: %s" \
                          % (sys.exc_info()[0],
                             sys.exc_info()[1])
            return result

        if not result.has_key('publication_type'): 
            result['publication_type'] = 'BookReference'

        return result


# Class instanciation
#InitializeClass(RefParser)

   
#def manage_addRefParser(self, REQUEST=None):
#    """ """
#    try:
#        self._setObject('ref', RefParser())
#    except:
#        return MessageDialog(
#            title='Bibliography tool warning message',
#            message='The parser you attempted to add already exists.',
#            action='manage_main')    
#    return self.manage_main(self, REQUEST)
