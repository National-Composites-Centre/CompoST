import h5py
from pydantic import BaseModel, Field
import json
import CompositeStandard as cs

#CURRENTLY DOESNT REALLY WORK -- UNDER DEVELOPMENT

# Function to save Pydantic object to HDF5
def save_to_hdf5(obj, file_name):
    # Convert Pydantic object to a dictionary
    obj_dict = obj.model_dump()  # Pydantic's model_dump() returns a dictionary

    # Create and save the dictionary to HDF5
    with h5py.File(file_name, 'w') as f:
        for key, value in obj_dict.items():
            # Store simple values directly
            if isinstance(value, (int, float, str)):
                f.attrs[key] = value
            # Store list or array data as datasets
            elif isinstance(value, list):
                f.create_dataset(key, data=value)


def load_from_hdf5(cls, file_name):
    with h5py.File(file_name, 'r') as f:
        # Create a dictionary from HDF5
        obj_dict = {key: f.attrs[key] if key in f.attrs else list(f[key]) for key in f.keys() | f.attrs.keys()}

    # Create the Pydantic object from the dictionary
    return cls(**obj_dict)


def testHDF5():

    D = cs.CompositeDB()

    # Save the object to HDF5
    save_to_hdf5(D, 'test.h5')

    # Load the object back from HDF5
    loaded_point = load_from_hdf5(cs.CompositeDB, 'test.h5')

    print(loaded_point)

testHDF5()