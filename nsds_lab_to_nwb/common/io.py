import json
import yaml
import csv

def read_yaml(file_path):
    with open(file_path, 'r') as stream:
        metadata_dict = yaml.safe_load(stream)
        metadata = json.loads(json.dumps(metadata_dict)) #, parse_int=str, parse_float=str)
        return metadata

def csv_to_dict(csv_file):
    with open(csv_file, mode='r') as infile:
        reader = csv.reader(infile)
        mydict = {rows[0]:rows[1] for rows in reader}
    # skip header
    if ('key', 'value') in mydict.items():
        mydict.pop('key')
    return mydict
