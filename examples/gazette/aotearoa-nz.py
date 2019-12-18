import csv
from taumahi import kōmiri_kupu

pūtuhi = csv.DictWriter(open('aotearoa-nz.csv', 'w'),
    fieldnames = ('id', 'name', 'status', 'feat_type', 'latitude', 'longitude', 'reo', 'maybe', 'other'))
pūtuhi.writeheader()

# Use the kōmiri_kupu function to count words of each language type in the
# placenames

for rārangi in csv.DictReader(open('gaz_names.csv')):
    reo = [sum(x.values()) for x in kōmiri_kupu(rārangi['name'])]
    pūtuhi.writerow(dict(id =rārangi['\ufeffname_id'],
        name = rārangi['name'],
        status = rārangi['status'],
        feat_type = rārangi['feat_type'],
        latitude = rārangi['crd_latitude'],
        longitude = rārangi['crd_longitude'],
        reo = reo[0],
        maybe = reo[1],
        other = reo[2]
        ))

