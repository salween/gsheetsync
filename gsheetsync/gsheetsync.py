# -*- coding: utf-8 -*-
"""Main module."""

import gspread

from lxml import etree
from lxml import objectify

et = etree.fromstring(open('/home/john/Downloads/export(37).xml').read())
types = et.find('.//Types')
parts = et.find('.//Parts')
content = et.find('.//Content')

def wks_from_contenttype(el):
    """
    Create a worksheet for an Orchard ContentType.

    Given a child of an Orchard <Types> element, generate a worksheet with
    columns for the fields. Pull in fields from <Parts> child elements.
    """
    headings = ['Id']
    wks = sheet.worksheet(el.tag) # TODO create if it doesn't exist
    for p in el:
        part = parts.find(p.tag)
        for field in part:
            headings.append('%s (%s)' % field.tag, field.get('DisplayName'))
    wks.insert_row(headings)
    return wks

def row_from_contentitem(el):
    """
    Create CSV for Orchard ContentItems.

    Given a child of an Orchard <Content> element, generate a row with
    columns for the fields.
    """
    i = el.get('Id')
    row = [i]
    for f in el:
        v = f.get('Text') or f.get('Value')
        row.append(v)
    return row

def rows_from_contentitems():
    for t in types:
        wks = wks_from_contenttype(t.tag)
        for el in content.findall(t.tag):
            wks.append_row(row_from_contentitem(el))


def upload_sheet(orchard_xml):
    pass

def export_sheet(sheet_name):
    pass
