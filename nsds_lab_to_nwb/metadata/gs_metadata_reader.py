#%%
import pandas as pd
import os
import yaml

class GSMetaDataReader():
    def __init__(self, path, block_id=None):
        self.path = path
        self.block_id = block_id
        if path.startswith('http'):
            self.online_flag = True
        else:
            self.online_flag = False
        self.raw_meta = None #dataframe
        self.raw_block = None #dataframe
        self.parsed_meta = None
        self.parsed_blocks = []
    
    def get_gsheet(self):
        return None
    
    def get_local_sheet(self):
        raw_meta = pd.read_csv(os.path.join(self.path, 'meta.csv'), 
                               delimiter=',',
                               skiprows=1, 
                               names=['a', 'values', 'b', 'c'],
                               index_col=1)
        raw_meta = raw_meta.iloc[:, 1]
        self.raw_meta = raw_meta
        
        self.raw_block = pd.read_csv(os.path.join(self.path, 'block.csv'),
                                     delimiter=',',
                                     header=2)
    
    def parse_meta(self):        
        parsed_meta = {'experiment':{}, 'other':{}, 'subject':{}}
        field_groups = list(parsed_meta.keys())
        all_fields = [['experimenter', 'lab', 'institution', 'date', 'time', 'experiment_description'],
                  ['pharmacology', 'surgery', 'surgery_outcome', 'surgery_notes'],
                  ['animal_number', 'animal_name', 'gender', 'weight']]
        
        for idx, fields in enumerate(all_fields):
            for field in fields:
                field_value = self.raw_meta[field]
                parsed_meta[field_groups[idx]][field] = field_value                  
        self.parsed_meta = parsed_meta        
    
    def parse_block(self, row):
        parsed_block = {'block': {}, 'device': {}}
        field_groups = list(parsed_block.keys())
        all_fields = [['block_id', 'device_ecog', 'device_poly', 'stim', 'clean_block', 'stim_response', 'notes'],
                      ['ecog_lat_loc', 'ecog_post_loc', 'poly_ap_loc', 'poly_dev_loc', 'ecog_placement', 'poly_placement']]
        for idx, fields in enumerate(all_fields):
            for field in fields:
                field_value = row[field]
                parsed_block[field_groups[idx]][field] = str(field_value)
        return parsed_block
    
    def parse_blocks(self):
        if self.block_id is None:
            row_ids = range(len(self.raw_block))
        else:
            row_ids = self.block_id       
        
        for idx in row_ids:
            row = self.raw_block.iloc[idx]
            parsed_block = self.parse_block(row)
            self.parsed_blocks.append(parsed_block)           
    
    def parse(self):
        self.parse_meta()
        self.parse_blocks()
        return None
    
    def dump_dict_as_yaml(self, file_name, my_dict):        
        with open(file_name, 'w') as file:
            yaml.dump(my_dict, file)   
    
    def dump_meta_as_yaml(self):
        self.dump_dict_as_yaml('meta.yaml', self.parsed_meta)
        
    def dump_blocks_as_yamls(self):
        for blk in self.parsed_blocks:
            print('test')
            yaml_name = 'block' + str(blk['block']['block_id']) + '.yaml'
            self.dump_dict_as_yaml(yaml_name, blk)           
    
    def dump_yamls(self):
        self.dump_meta_as_yaml()
        self.dump_blocks_as_yamls()
    
    def make(self):
        if self.online_flag:
            self.get_gsheet()
        else:
            self.get_local_sheet()
        
        self.parse()      
        self.dump_yamls()
        
            
#%%

obj = GSMetaDataReader('/home/jhermiz/software/nsds_lab_to_nwb/nsds_lab_to_nwb/metadata')
obj.make()
# obj.get_local_sheet()
# df = obj.raw_block
# df.head()
# obj.parse_blocks()
# blks = obj.parsed_blocks
# print(blks)

# %%

# import yaml

# with open('test.yaml', 'w') as file:
#     documents = yaml.dump(my_dict, file)

# %%


