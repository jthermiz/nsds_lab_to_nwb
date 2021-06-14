import io
import json
import yaml
import csv


# --- yaml ---

class MyDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)

def write_yaml(yml_path, data, access_mode='w', default_flow_style=False, sort_keys=False):
    # note: additional kwargs may not work in older versions of pyyaml
    with io.open(yml_path, access_mode) as fh:
        yaml.dump(data, fh,
                  Dumper=MyDumper,
                  default_flow_style=default_flow_style,
                  sort_keys=sort_keys)

def read_yaml(file_path):
    with open(file_path, 'r') as stream:
        content_dict = yaml.safe_load(stream)
        content = json.loads(json.dumps(content_dict)) #, parse_int=str, parse_float=str)
        return content


# --- csv ---

def csv_to_dict(csv_file):
    with open(csv_file, mode='r') as infile:
        reader = csv.reader(infile)
        mydict = {rows[0]:rows[1] for rows in reader}
    # skip header
    if ('key', 'value') in mydict.items():
        mydict.pop('key')
    return mydict
