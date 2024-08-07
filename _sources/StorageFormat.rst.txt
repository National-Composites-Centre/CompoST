StorageFormat
=============

The format is based around Python class definition. This allows for some flexibility, namely it allows to store in efficient formats such as HDF5, or human readable formats, such as JSON. The important aspect is that this format stays consistent when loaded in Python, or saved from Python.



JSON
----
Jsonic library used for serialization of Pydantic based Classes. Dedicated script written which simplifies the natively exported JSON file to improve human readability, without affecting the values stored (clean_json within 'Utilities.py')



HDF5
----

(TODO)