class Dataset():
    def __init__(self, data_path, animal_name, block, **path_kwargs):
        self.data_path = data_path
        self.animal_name = animal_name
        self.block = block

        # store all paths
        for path_key, path_value in path_kwargs.items():
            setattr(self, path_key, path_value)
