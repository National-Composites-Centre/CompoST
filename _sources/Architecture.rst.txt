Architecture
============

.. image:: NCC-TEC-4376CompositeDigitalTwinClassMap_wip_0.61.*
    :width: 1000
	
On the figure above, arrows point from an object 1 to object 2, where object 1 inherits from object 2.

The figure is also work-in-progress. The outline titled "mostly fixed" houses the objects that have been implemented and used. These will hopefully see only minor adjustments. Objects outside this area might end up being standardised differently than currently suggested.

All fields are optional unless otherwise specified, or unless required to construct specific object.

Where the same attribute is being called in parent and child (e.g. axis being referenced in ply, and in some of corresponding cut pieces), the more detailed (child) component supersedes the corresponding parent definition.

CompositeDB object is the main object of the Composite Standard. All objects are stored in lists named all***.  
	
	
.. py:function:: CompositeStandard.CompositeDB()

    All elements and all geometry are all stored here and used elsewhere as refrence
    Points are stored withing those, as referencing is not efficient
	
	:param name: str - name
	:param rootElements: list - List of CompositeElement type objects
	:param allEvents: list  - List of "events" objects - all = exhaustive list
	:param allGeometry: list - list of "GeometricElement" objects - all = exhaustive list
	:param allStages: list - manuf process - all = exhaustive list
	:param allMaterials: list - List of "Material" objects - all = exhaustive list
	:param allAxisSystems: dict -
	:param fileMetadata: object - list of all "axisSystems" objects = exhaustive list
