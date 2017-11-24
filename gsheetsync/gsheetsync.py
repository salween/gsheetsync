# -*- coding: utf-8 -*-
"""Main module."""

import json
import gspread
# from oauth2client.client import SignedJwtAssertionCredentials
from oauth2client.service_account import ServiceAccountCredentials

from lxml import etree
from lxml import objectify

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]

json_key = json.load(open('gsheetsync-bac80241bd44.json'))
credentials = ServiceAccountCredentials.from_json_keyfile_name('gsheetsync-bac80241bd44.json', scope)

gc = gspread.authorize(credentials)

sheet = gc.open("Test from gsheetsync")

et = etree.fromstring(open('orchard-content.xml').read())
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

    try:
        wks = sheet.worksheet(el.tag)
    except gspread.exceptions.WorksheetNotFound:
        wks = sheet.add_worksheet(el.tag, 1000, 26)

    for p in el:
        part = parts.find(p.tag)
        if part:
            for field in part:
                headings.append('%s (%s)' % field.tag, field.get('DisplayName'))
    wks.insert_row(headings)
    return wks

for el in types.getchildren():
    wks_from_contenttype(el)

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
