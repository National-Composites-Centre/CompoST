Mapping and references
======================

(Under development)

This documentation will advice on how to translate between spline definitions and element definitions (for example).


Reference Surface
-----------------
 
On default surface should be provided within the CAD reference, usually provided as step file: see parameter ``cadFile`` in :func:`CompositeStandard.FileMetadata`. Currently ,in ideal case 
only one main surface is loaded from the provided step file, corresponding to the tool surface. 

It is the intention of the developers to allow for specific references to hash numbers in the step file. This way user would be able to select specific surfaces in STEP file and 
allocate them to composite objects. However, this will require extensive exploration to understand how this might affect loading/unloading of the standard, and likely dedicated scripts
to manage accuracy will need to be implemented when saving/re-saving files from CAD systems.


Material Knockdown Properties
-----------------------------

The material knockdown properties are stored as a standard material. For example, if wrinkle is identified, the effective material is calculated based on severity of the wrinkle and original local material properties.

This material is then appended as ``effMaterial`` in :func:`CompositeStandard.Defect`. In practice, this can then be used to implement into FE model with new properties for this specific area, overwriting the material properties
noted at ply level (for example).

   
IDs
---

Every object belonging to :py:meth:`~CompositeStandard.CompositeDBItem.get` family can have 'ID' parameter attributed to it. This allows for referencing geometries and composite elements without re-creating them. The most common usage of this is when 'CompositeStandard.Piece' uses parameter splineRelimitation to signifcy edge of the composite piece, this parameter is simply and integer - 'ID', and corresponding spline can be found in GeometricElement`


IDs are not compulsory for any object, but it is highly recommended that most objects are given IDs, as that will facilitaty any re-use. Exceptions are objects that will definitely not see reuse, such as point only existing to create a complex spline.


Duplication of properties
-------------------------

Many objects share parameters, and can become each others parent/child. This may lead to situation where paramters are duplicated. This is intended so that one can define a parameter for a complete sequence, but than specify differing
parameter for a specific ply.

The rule for which parameter takes effect is as follows: Where the same attribute is being called in parent and child (e.g. axis being referenced in ply, and in some of corresponding cut pieces), the more detailed (child) component supersedes the corresponding parent definition.

