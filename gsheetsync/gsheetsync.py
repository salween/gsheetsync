# -*- coding: utf-8 -*-
"""Main module."""

from datetime import datetime
import glob
from lxml import etree
from lxml import objectify
import unicodecsv as csv
import hashlib

Element = objectify.Element
E = objectify.E
nowstr = datetime.now().strftime('%Y-%m-%d')

et = etree.fromstring(open('export.xml').read())
content = et.find('.//Content')
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
    header = get_header(ct)

    with open('{0}.csv'.format(ct.tag), 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()

        for item in content.findall(ct.tag):
            i = item.get('Id')
            row = {'IdentityPart:Identifier': i.split('=')[1]}
            for field in item:
                for attribute, value in field.items():
                    row[field_to_header(field, attribute)] = value
            writer.writerow(row)

def csvs_from_contenttypes():
    types = et.find('.//Types')
    for ct in types:
        csv_from_contenttype(ct)

def sha_id(row):
    keys = list(row.keys())
    keys.sort()
    values = [row[k] for k in keys]
    sha1 = hashlib.sha1()
    sha1.update(repr(values).encode('utf-8'))
    return sha1.hexdigest()

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
        ct = fn.replace('.csv', '')
        with open(fn, 'rb') as csvfile:
            data = csv.DictReader(csvfile)
            for row in data:
                item = {}
                for fieldattr, value in row.items():
                    tagname, attribute = fieldattr.split(':')
                    if value:
                        attr_values = item.setdefault(tagname, {})
                        attr_values[attribute] = value
                if not item.get('IdentityPart'):
                    item['IdentityPart'] = {'Identifier': sha_id(row)}
                el = getattr(E, ct)(
                    *[getattr(E, tag)(attributes) for tag, attributes in item.items()],
                    Id="/Identifier=%s"%item['IdentityPart']['Identifier'],
                    Status="Published"
                )
                orchard.Content.append(el)

    objectify.deannotate(orchard, cleanup_namespaces=True)
    ff = open('import.xml', 'wb')
    ff.write(etree.tostring(orchard, pretty_print=True))
    ff.close()






