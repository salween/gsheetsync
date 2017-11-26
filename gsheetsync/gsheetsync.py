# -*- coding: utf-8 -*-
"""Main module."""

from lxml import etree
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import json
from tinydb import TinyDB, Query, where

def connect_sheet(title):
    """
    Connect to a Google Sheet
    """
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]

    json_key = json.load(open('gsheetsync-bac80241bd44.json'))
    credentials = ServiceAccountCredentials.from_json_keyfile_name('gsheetsync-bac80241bd44.json', scope)

    gc = gspread.authorize(credentials)

    try:
        sheet = gc.open(title)
    except gspread.exceptions.SpreadsheetNotFound:
        sheet = gc.create(title)

    return sheet

et = etree.fromstring(open('orchard-content.xml').read())
types = et.find('.//Types')
parts = et.find('.//Parts')
content = et.find('.//Content')

db = TinyDB('db.json')

def schema_from_contenttype(el):
    """
    Generate schema tables
    """
    print('type', el.tag)
    table = db.table("schemas")
    fields = {'item_id': 'Identity', 'contenttype': el.tag}
    for p in el:
        part = parts.find(p.tag)
        print('  part', p.tag)
        if part is not None:
            for field in part:
                print('    field', field.tag)
                fields[field.tag] = field.get('DisplayName')
    table.upsert(fields, where('contenttype') == el.tag)

def wks_from_contenttype(el):
    """
    Create a worksheet for an Orchard ContentType.

    Given a child of an Orchard <Types> element, generate a worksheet with
    columns for the fields. Pull in fields from <Parts> child elements.
    """
    headings = ['Id']

    try:
        wks = sheet.worksheet(el.tag)
        # TODO: update header line
        return wks
    except gspread.exceptions.WorksheetNotFound:
        wks = sheet.add_worksheet(el.tag, 1000, 26)

    print('type', el.tag)
    for p in el:
        part = parts.find(p.tag)
        print('  part', p.tag)
        if part is not None:
            for field in part:
                print('    field', field.tag)
                headings.append('{0} ({1})'.format(field.tag, field.get('DisplayName')))
    wks.insert_row(headings)
    return wks


def row_from_contentitem(el):
    """
    Create rows for Orchard ContentItems.

    Given a child of an Orchard <Content> element, generate a row with
    columns for the fields.
    """
    i = el.get('Id')
    # schema = db.table('schemas').get(where('contenttype') == el.tag)
    # values = {k:'' for k,v in schema.items()}
    table = db.table(el.tag)
    values = {'item_id': i}
    for f in el:
        for k,v in f.items():
            values['{0}:{1}'.format(f.tag, k)] = v
    # values.update({f.tag: f.get('Text') or f.get('Value') for f in el})
    table.upsert(values, where('item_id')==i)

def rows_from_contentitems(ct):
    # wks = wks_from_contenttype(ct)
    print('  content for', ct.tag)
    for el in content.findall(ct.tag):
        row_from_contentitem(el)


def upload_sheet(orchard_xml):
    pass

def export_sheet(sheet_name):
    pass

# for el in types.getchildren():
    # wks_from_contenttype(el)

for ct in types.getchildren():
    schema_from_contenttype(ct)
    rows_from_contentitems(ct)
