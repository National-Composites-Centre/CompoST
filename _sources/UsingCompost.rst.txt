UsingCompost
============

This page provides instructions on how to use CompoST.

Eventually CompoST will become pip-installable library, but for now it is recommended to clone the repository and copy "CompositeStandard.py" file into your project.


Installation
--------------
Compost can be installed into an environemnt using pip, as per below.

.. code-block:: bash

	pip install git+https://github.com/National-Composites-Centre/CompoST.git
	
The recommended import to a Python script looks as follows:

.. code-block:: Python

	from CompoST import CompositeStandard as cs


Libraries automatically installed with CompoST: pydantic, jsonic ,numpy

"numpy" is required for generation of axis systems. "jsonic" is used for serializing and desirializing the objects into and from JSON. "pydantic" helps with class definitions and validations.




Loading Files
-------------

Loading CompoST JSON files is very simple in Python, the following code shows an example. The following code is applicable from 0.7.5 onwards.

.. code-block:: python

	from CompoST import CompositeStandard as cs
	D = cs.Open(CompoST_file,path=path)

Thie opens "CompoST_file" located at "path", and assigns it variable "D". The funciton also re-links any objects with same ID so these automatically update simultaneously when changed.

For older versions opening, deserializing and re-linking is done as individual operations:

.. code-block:: python

    from jsonic import serialize, deserialize
    #open file
    with open(IMPORTED_JSON_FILE,"r") as in_file:
        json_str= in_file.read()
    
    D = deserialize(json_str,string_input=True)
    
    #Optional - makes sure that any objects that were linked before serialization, will be re-linked - and can then be edited simultaneously.
    #This requires further testing - might have minor bugs.
    from Utilities import reLink
    D = reLink(D)
	
Now "D" can be interogated according to `CompositeStandard` classes.

Loading the file to any other language/software that accepts JSON schema should be also possible, but this has seen minimal testing (TODO).

The optional :func:`Utilities.reLink` function exists as JSON natively does not store information on which objects were copies of each other (i.e. stored in memory as one).
This function re-creates these links based on `ID` parameters, as the copy-based objects will share `ID`. Of course, if `ID` definition was omitted, this function will not work.

Saving Files
------------
To save the CompoST data structure it first has to be initiated. This can either be done by loading existent file (as per above), or using the following:

.. code-block:: python

    import CompositeStandard as cs
    d = cs.CompositeDB()
    d.fileMetadata.lastModified = "10/07/2024"
    d.name = "NewPart"
	
The date and name are included only as example, it is up to user which of the variables available are useful to them.

After all required information has been saved somewhere in the tree belonging to `CompositeDB` object, the following code serializes the data into JSON string and saves it. The function also adds line-breaks to the file so
that it becomes human readable to some extent.

.. code-block:: python

	from CompoST import CompositeStandard as cs
	#D is the CompositeDB object
	cs.Save(D,filename,path=path)
	
The funciton takes the CompoST main object, filename and path. If path is not provided it will be saved in current directory.

In older versions the expanded saving method is as follows:

.. code-block:: python

    from jsonic import serialize, deserialize
    # Convert dictionary to JSON string
    json_str = serialize(d, string_output = True)

    #Optional - makes JSON human readable
    json_str = cleandict(json_str)

    #save as file
    with open('YOUR_SAVED_JSON_FILE', 'w') as out_file:
        out_file.write(json_str)
		
The `cleandict` funciton can be find in main CompoST repository under `Utilities.py` module. It is recommended that this step is added for human readability.

Utility Scripts
---------------

Sister repository has been created to store various utility scripts. These scrips are only going to be relevant for specific users of CompoST, and hence it is not appropriate to house the scripts here.

https://github.com/National-Composites-Centre/CST_utils 

