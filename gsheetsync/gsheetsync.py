# -*- coding: utf-8 -*-
"""Main module."""

import glob
from lxml import etree
import unicodecsv as csv

et = etree.fromstring(open('orchard-content.xml').read())
# types = et.find('.//Types')
# parts = et.find('.//Parts')

def field_to_header(field, attribute):
    return '{0}:{1}'.format(field.tag, attribute)

def get_header(ct):
    """Get header for a content type, by crawling all the content items
    """
    header_dict = {}
    for item in content.findall(ct.tag):
        for field in item:
            for attribute in field.keys():
                header_dict[field_to_header(field, attribute)] = None
    return sorted(header_dict.keys())

def csv_from_contenttype(ct):
    """
    Create a CSV file for an Orchard ContentType.

    Given a child of an Orchard <Types> element, generate a worksheet with
    columns for the fields. Pull in fields from <Parts> child elements.
    """
    header = ['Id']
    header.extend(get_header(ct))

    with open('{0}.csv'.format(el.tag), 'wb') as csvfile:
        print(csvfile.name)
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()

        for item in content.findall(ct.tag):
            i = item.get('Id')
            row = {'Id': i}
            for field in item:
                for attribute, value in field.items():
                    row[field_to_header(field, attribute)] = value
            writer.writerow(row)

def csvs_from_contenttypes():
    content = et.find('.//Content')
    for ct in content:
        csv_from_contenttype(ct)

def xml_from_csv():
    orchard = Element('Orchard')
    orchard.Recipe = E.Recipe(E.ExportUtc(nowstr))
    # orchard.Feature = E.Feature(enable=', '.join(site_description[0]['Features']))
    # orchard.Settings = E.Settings(*list(genSettings(site_description[1]['Settings'])))
    orchard.Migration = E.Migration(features="*")
    # orchard.Command = E.Command("""
    #     layer create Default /LayerRule:"true" /Description:"The widgets in this layer are displayed on all pages"
    #     ...
    #     """)

    csv_filenames = glob.glob("*.csv")
    orchard.Content = E.Content()
    for fn in csv_filenames:
        with open(fn, 'rb') as csvfile:
            data = csv.DictReader(csvfile)
            for row in data:
                item = {}
                for fieldattr, value in row.items():
                    tagname, attribute = fieldattr.split(':')
                    attr_values = item.setdefault(tagname, {})
                    attr_values[attribute] = value
                el = E.get(fn)
                for field, attrs in item.items():






return data
