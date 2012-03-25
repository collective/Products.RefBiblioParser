# -*- coding: utf-8 -*-
############################################################################
#                                                                          #
#             copyright (c) 2004 ITB, Humboldt-University Berlin           #
#             written by: Raphael Ritz, r.ritz@biologie.hu-berlin.de       #
#                                                                          #
############################################################################

"""RefRenderer class"""

# Python stuff
import os

# zope3 imports
from zope.component import getMultiAdapter
from zope.component import queryAdapter
from zope.interface import implements
from zope.publisher.browser import TestRequest

# CMF stuff
from Products.CMFCore.utils import getToolByName

# Bibliography stuff
from bibliograph.rendering.renderers.base import BaseRenderer
from bibliograph.rendering.interfaces import IReferenceRenderer, IBibliographyRenderer
from bibliograph.core.interfaces import IBibliographyExport
from bibliograph.rendering.utility import UtilityBaseClass

class RefRendererView(BaseRenderer):
    """
    specific Ref renderer
    """
    implements(IReferenceRenderer)
    file_extension = 'REF'
    def render(self, title_force_uppercase=False, omit_fields=[],
              msdos_eol_style=None, # not used
              resolve_unicode=None, # not used
              output_encoding=None, # not used
              ):
        """
        renders a BibliographyEntry object in Ref format
        """
        entry = self.context
        ref = {}
        ref['A'] = "%A " + entry.Authors(sep="\n%A ",
                                         lastsep="\n%A ",
                                         abbrev=0,
                                         lastnamefirst=1)

        value = self.AuthorURLs(entry)
        if value:
          ref['O'] = "\n%O " + '\n%O '.join(''.join(value).split('\n'))

        value = entry.getPublication_year().strip()
        if value:
          if value!='':
            ref['D'] = "\n%D" + value.strip()
          elif 'in press' in entry.getAbstract():
            ref['D'] = "in press"
          else:
            ref['D'] = "n.d."

        try:
          value = entry.getType()
        except:
          value =""
        if value:
          ref['R'] = "\n%R " + value.strip()

        try:
          value = entry.Title()
        except:
          value =""
        if value:
          if not ref.has_key('R') :
           for key in ['acte', 'thesis', 'eindwerk', 'thèse', 'proceedings', 'akte']:
            if key in value:
              value.split(':')
              ref['T'] = "\n%T " + value[0].strip()
              ref['R'] = "\n%R " + value[1].strip()
              break
          if not ref.has_key('T') :
            ref['T'] = "\n%T " + value.strip()

        if not ref.has_key('R') :
         try:
           value = entry.getNote()
         except:
           value =""
         if value:
          for key in ['acte', 'thesis', 'eindwerk', 'thèse', 'proceedings', 'akte']:
           if key in value:
            for svalue in value.split('\n'):
             for key2 in ['acte', 'thesis', 'eindwerk', 'thèse', 'proceedings', 'akte']:
              if key2 in svalue:
               ref['R'] = "/n%R " + svalue.strip()
               break

        try:
          value = entry.getBooktitle()
        except:
          value =""
        if value:
          if not ref.has_key('R') :
           for key in ['acte', 'thesis', 'eindwerk', 'thèse', 'proceedings', 'akte']:
            if key in value:
              value.split(':')
              ref['B'] = "\n%B " + value[0].strip()
              ref['R'] = "\n%R " + value[1].strip()
              break
          if not ref.has_key('B') :
            ref['B'] = "\n%B " + value.strip()

        try:
          value = entry.getJournal()
        except:
          value =""
        if value:
          ref['J'] = "\n%J " + value.strip()

        try:
          value = entry.getPublisher()
        except:
          value =""
        if value:
          ref['I'] = "\n%I " + value.strip()

        try:
          value = entry.getCity()
        except:
          value =""
        if value:
          ref['C'] = "\n%C " + value.strip()

        try:
          value = entry.getVolume()
        except:
          value =""
        if value:
          ref['V'] = "\n%V " + value.strip()

        try:
          value = entry.getNumber()
        except:
          value =""
        if value:
          ref['N'] = "\n%N " + value.strip()

        try:
          value = entry.getPages()
        except:
          value =""
        if value:
          ref['P'] = "\n%P " + value.strip()

        try:
          value = entry.getAbstract()
        except:
          value =""
        if value:
          if not ref.has_key('O') :
            ref['O'] = "\n%O " + '\n%O '.join(''.join(value).split('\n'))
          else:
            ref['O'] += "\n%O " + '\n%O '.join(''.join(value).split('\n'))

        try:
          value = entry.getNote()
        except:
          value=""
        if value:
          svalue = value.split('\n')
          value=""
          for key in svalue:
            for key2 in ['acte', 'thesis', 'eindwerk', 'thèse', 'proceedings', 'akte', 'in press', 'automatic ref import']:
              if key2 in key:
                key = ''
                break
            if key != '':
              value += key.strip() + '\n'
          ref['X'] = "/n%X " + value.strip()

        try:
          value = entry.getURL()
        except:
          value =""
        if value:
          if not ref.has_key('O') :
            ref['O'] = "\n%O " + '\n%O '.join(''.join(value).split('\n'))
          else:
            ref['O'] += "\n%O " + '\n%O '.join(''.join(value).split('\n'))

        try:
          value = entry.getSubject()
        except:
          value =""
        if value:
          ref['K'] = "\n%K " + '\n%K '.join(''.join(value).split('\n'))

        refer=''
        for key in ['A', 'D', 'T', 'R', 'I', 'K', 'J', 'V', 'P', 'B', 'C', 'E', 'X', 'O', 'N', 'M', 'Z', ]:
          refer += ref.get(key, '')
        return refer + '\n\n'

    def AuthorURLs(self, entry):
        """a string with all the known author's URLs;
        helper method for bibtex output"""
        a_list = entry.getAuthorList()
        a_URLs = ''
        for a in a_list:
            url = a.get('homepage', ' ')
            if url != ' ':
              a_URLs += "%s and " % url
        if a_URLs != '':
          a_URLs = a_URLs[:-5]
        return a_URLs[:-5]

class RefRenderer(UtilityBaseClass):
    """An implementation of IBibliographyRenderer that renders to ref.
    """
    implements(IBibliographyRenderer)
    default_encoding = u''
    __name__ = u'REF'
    source_format = u''
    target_format = u'REF'
    description = u'Export to native REF format'
    view_name = u'ref'
    available = True
    enabled = True

    def render(self, objects,
                     title_force_uppercase=False,
                     output_encoding=None,
                     msdos_eol_style=False,
                     omit_fields_mapping={}):
        """ Export a bunch of bibliographic entries in ref format"""
        if isinstance(objects, (list, tuple)):
            context = objects[0]
        else:
            context = objects

        if not IBibliographyExport.providedBy(context):
            try:
                context = context.aq_parent
            except AttributeError:
                pass


        object = entry = self.context
        bib_tool = getToolByName(object, 'portal_bibliography')
        ref_types = bib_tool.getReferenceTypes()
        if object.portal_type in ref_types:
            return self.renderEntry(object)
        for obj in entries:
            ref = queryAdapter(obj, interface=IBibliographicReference,
                                    name=self.__name__)
            if ref is None:
                # if there is no named adapter, get the default adapter
                # compatibility with older versions
                ref = IBibliographicReference(obj, None)
            if ref is None:
                continue

            # do rendering for entry
            view = getMultiAdapter((ref, request), name=self.view_name)
            omit_fields = omit_fields_mapping.get(ref.publication_type, [])
            bibtex_string = view.render(title_force_uppercase=title_force_uppercase,
                                        omit_fields=omit_fields
                                        )
            rendered.append(bibtex_string)

        rendered = ''.join(rendered)
        if msdos_eol_style:
            rendered = rendered.replace('\n', '\r\n')
        return rendered
        if object.isPrincipiaFolderish:
            entries = object.contentValues(ref_types)
            rendered = [self.renderEntry(entry) \
                        for entry in entries]
            return ''.join(rendered)
        return ''

