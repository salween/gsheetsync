# -*- coding: utf-8 -*-

"""Console script for gsheetsync."""

from pathlib import Path
import click
from gsheetsync import gsheetsync


@click.command()
@click.argument('infile', type=click.File('rb'))
def main(infile):
    """Specify an XML file to generate an XSLX file, or an XSLX file to generate an XML file.
    This script generates intermediate CSV files.
    """
    if not infile:
        print("No file specified")
        return
    if Path(infile.name).suffix.lower() == '.xml':
        gsheetsync.xlsx_from_xml(infile)
    elif Path(infile.name).suffix.lower() == '.xlsx':
        gsheetsync.xml_from_xlsx(infile)
    else:
        print("Unrecognized file type")


if __name__ == "__main__":
    main()

