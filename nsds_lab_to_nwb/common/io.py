import json
import yaml

def read_yaml(file_path):
    with open(file_path, 'r') as stream:
        metadata_dict = yaml.safe_load(stream)
        metadata = json.loads(json.dumps(metadata_dict)) #, parse_int=str, parse_float=str)
        return metadata
