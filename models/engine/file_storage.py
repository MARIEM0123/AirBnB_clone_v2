#!/usr/bin/python3
"""definition of the hbnb DB file storage management"""
import json
import os
from importlib import import_module


class FileStorage:
    """File storage in the JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def __init__(self):
        """Initialization of the  FileStorage instance"""
        self.model_classes = {
            'BaseModel': import_module('models.base_model').BaseModel,
            'User': import_module('models.user').User,
            'State': import_module('models.state').State,
            'City': import_module('models.city').City,
            'Amenity': import_module('models.amenity').Amenity,
            'Place': import_module('models.place').Place,
            'Review': import_module('models.review').Review
        }

    def all(self, cls=None):
        """Display the dictionary in storage before updating"""
        if cls is None:
            return self.__objects
        else:
            fdt = {}
            for K, V in self.__objects.items():
                if type(V) is cls:
                    fdt[K] = V
            return fdt

    def delete(self, obj=None):
        """the function to delete the obj from the dict"""
        if obj is not None:
            objk = obj.to_dict()['__class__'] + '.' + obj.id
            if objk in self.__objects.keys():
                del self.__objects[objk]

    def new(self, obj):
        """funct to add new obj to storage dict"""
        self.__objects.update(
            {obj.to_dict()['__class__'] + '.' + obj.id: obj}
        )

    def save(self):
        """the function to save storage dict to file"""
        with open(self.__file_path, 'w') as file:
            p = {}
            for K, V in self.__objects.items():
                p[K] = V.to_dict()
            json.dump(p, file)

    def reload(self):
        """Add storage dict from file"""
        cls = self.model_classes
        if os.path.isfile(self.__file_path):
            P = {}
            with open(self.__file_path, 'r') as file:
                P = json.load(file)
                for K, V in P.items():
                    self.all()[K] = cls[V['__class__']](**V)

    def close(self):
        """function to close the storage engine."""
        self.reload()
