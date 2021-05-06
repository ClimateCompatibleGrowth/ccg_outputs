"""Retrieves outputs from Zenodo CCG group

dict_keys(['creator', 'date', 'description', 'identifier', 'language', 'relation', 'rights', 'subject', 'title', 'type'])

"""
from csv import writer
from sickle import Sickle

URL = """https://zenodo.org/oai2d?verb=ListRecords&set=user-ccg&metadataPrefix=oai_dc"""
si = Sickle(URL)
records = si.ListRecords(metadataPrefix='oai_dc')

repositories = {}
for record in records:
    md = record.metadata
    relation = md['relation'][0]
    if relation in repositories:
        stamp = record.header.datestamp
        exist_stamp = repositories[relation].header.datestamp

        if stamp > exist_stamp:
            repositories[relation] = record
    else:
        repositories[relation] = record

citations = []
for record in repositories.values():
    md = record.metadata

    try:
        title = md['title'][0]
    except KeyError:
        title = ''

    output_type = md['type'][1]

    authors = []
    for author in md['creator']:
        try:
            lastname, firstname = author.split(",")
        except ValueError:
            firstname, lastname = author.split(" ")
        initial = firstname.strip()[0]
        authors.append("{}, {}.".format(lastname, initial))

    year = md['date'][0].strip()[0:4]

    citation = "{}, {}, {}, {}, {}, {}".format(", ".join(authors), year, title, md['date'][0], md['identifier'][0], output_type)
    citations.append(citation)

with open('outputs.txt', 'w') as textfile:
    for x in citations:
        textfile.write("{}\n".format(x))
