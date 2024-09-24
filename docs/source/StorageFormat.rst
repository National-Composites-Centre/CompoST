StorageFormat
=============

The format is based around Python class definition. This allows for some flexibility, namely it allows to store in efficient formats such as HDF5, or human readable formats, such as JSON. The important aspect is that this format stays consistent when loaded in Python, or saved from Python.



JSON
----
Jsonic library used for serialization of Pydantic based Classes. Dedicated script written which simplifies the natively exported JSON file to improve human readability, without affecting the values stored (clean_json within 'Utilities.py')

The main benefit of JSON is human readability. For new users of CompoST this allows for easier review of information stored.

JSON format has some limitations. The most significant limitation is the lack of ability to store referencing links, between object and it's copy. While the object referencing can be leveraged in CompoST before serialization, JSON
does not have a native method for storing these links. The most relevant example is :func:`CompositeStandard.Defect` object stored under specific :func:`CompositeStandard.CompositeDBItem` as "defects" parameter. The standard use
of CompoST would suggest copy of this object would also be present in parameter `allDefects`. When one of these 2 objects is edited, initially both objects are edited. Once serialized into JSON and re-imported this link is removed.
From serialization onwards both object have to be edited separately, which is inconvenient and may cause confusion down the line. To minimize the potential confusion it is recommended that either objects are stored only in one place, 
or the `ID` parameter is diligently used, so that the link can be infered later, and either created on deserialization or at least visible to the user.

For re-creating these links after deserialization :func:`Utilities.reLink` function was created. This identifies duplicate `ID`s in all relevant lists, and re-generates the links for consistent, and more practical editing of Python
objects.


HDF5
----

HDF5 serialization and re-import are theoretically possible, but most up-to-date development has been done using JSON.

One of the main benefits of HDF5 is that it can better follow full Python object functionality, for example links between object copies can be maintained through export/import, serializtion/deserialization. 

Main downside is that HDF5 is not human readable. This is not only problem for new users and their ease of use, but also in terms of troubleshooting of any potential serialization issues.