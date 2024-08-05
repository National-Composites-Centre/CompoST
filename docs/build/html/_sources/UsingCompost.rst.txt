UsingCompost
============

This page provides instructions on how to use CompoST.

Eventually CompoST will become pip-installable library, but for now it is recommended to clone the repository and copy "CompositeStandard.py" file into your project.


Pre-requisites
==============

Libraries to install: Pydantic, jsonic 

.. code-block:: bash

	pip install py-jsonic
	pip install pydantic

(more information tbd TODO)

Loading Files
=============

Loading CompoST JSON files is very simple in Python, the following code shows an example.


.. code-block:: python

    from jsonic import serialize, deserialize
    #open file
    with open(IMPORTED_JSON_FILE,"r") as in_file:
        json_str= in_file.read()
    
    D = deserialize(json_str,string_input=True)
	
Now "D" can be interogated according to `CompositeStandard` classes.

Loading the file to any other language/software that accepts JSON schema should be also possible, but this has seen minimal testing (TODO).

Saving Files
============
To save the CompoST data structure it first has to be initiated. This can either be done by loading existent file (as per above), or using the following:

.. code-block:: python

    import CompositeStandard as cs
    d = cs.CompositeDB()
    d.fileMetadata.lastModified = "10/07/2024"
    d.name = "NewPart"
	
The date and name are included only as example, it is up to user which of the variables available are useful to them.

Guide on how build the data format (LINK - pending - TODO)

After all required information has been saved somewhere in the tree belonging to `CompositeDB` object, the following code serializes the data into JSON string and saves it.

.. code-block:: python

    from jsonic import serialize, deserialize
    # Convert dictionary to JSON string
    json_str = serialize(d, string_output = True)

    #Optional - makes JSON human readable
    #json_str = cleandict(json_str)

    #save as file
    with open('YOUR_SAVED_JSON_FILE', 'w') as out_file:
        out_file.write(json_str)
		
The `cleandict` funciton can be find in main CompoST repository under `Utilities.py` module. It is recommended that this step is added for human readability.

Utility Scripts
===============

(TODO - link to sister repository with potentially useful scripts)