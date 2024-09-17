Mapping and references
======================

(Under development)

This documentation will advice on how to translate between spline definitions and element definitions (for example).

Assembly Order
--------------
The objects are ordered from tool surface, as they appear in the ``AllComposite`` list within :func:`CompositeStandard.CompositeDB`. This is the most practical way to structure composite object for most approaches. It might require additional operations when replacing a ply,
as the location will have to be retreived first, but should be convenient in most cases. Dedicated explicit numbering of plies, core, etc is currrently not deemed necessary.


Reference Surface
-----------------
 
On default surface should be provided within the CAD reference, usually provided as step file: see parameter ``cadFile`` in :func:`CompositeStandard.FileMetadata`. Currently ,in ideal case 
only one main surface is loaded from the provided step file, corresponding to the tool surface. 

It is the intention of the developers to allow for specific references to hash numbers in the step file. This way user would be able to select specific surfaces in STEP file and 
allocate them to composite objects. However, this will require extensive exploration to understand how this might affect loading/unloading of the standard, and likely dedicated scripts
to manage accuracy will need to be implemented when saving/re-saving files from CAD systems.


Spline Generation
-----------------

Standard is designed to work with multiple different software that generate or export splines, some of which do not provide information on how splines are generated mathematically. 
Therefore the practical approach is to increase number of points stored in order to provide more precise spline for delimiation. This is currently considered sufficient for all 
forseen applications. 

Some delimations, however, will require spline breaks. Those can be specified by ``breaks`` parameter in :func:`CompositeStandard.Spline`. The most common purpose for these are part/ply corners.
These should help wherever the used software struggles to provide reasonable continuity betwen points.


   
IDs
---

Every object belonging to :py:meth:`~CompositeStandard.CompositeDBItem.get` family can have 'ID' parameter attributed to it. This allows for referencing geometries and composite elements without re-creating them. The most common usage of this is when 'CompositeStandard.Piece' uses parameter splineRelimitation to signifcy edge of the composite piece, this parameter is simply and integer - 'ID', and corresponding spline can be found in GeometricElement`


IDs are not compulsory for any object, but it is highly recommended that most objects are given IDs, as that will facilitaty any re-use. Exceptions are objects that will definitely not see reuse, such as point only existing to create a complex spline.


