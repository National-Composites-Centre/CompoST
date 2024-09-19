Logic and philosophy
====================


Assembly Order
--------------
The objects are ordered from tool surface, as they appear in the ``AllComposite`` list within :func:`CompositeStandard.CompositeDB`. This is the most practical way to structure composite object for most approaches. It might require additional operations when replacing a ply,
as the location will have to be retreived first, but should be convenient in most cases. Dedicated explicit numbering of plies, core, etc is currrently not deemed necessary.


Variable duplication
--------------------

Multiple different objects in the hierarchy can have the same properties. For instance :func:`CompositeStandard.Sequence` shares many properties with :func:`CompositeStandard.Ply`, for example 'material'. This allows for greater flexiblity. Users can store a sequence that consists of multople plies, or simply store multiple plies.
The main benefit of sequence would typically be specifying all properties that are common only once. If one plies differs (for example different material), user does not have to use ply only definition but can simply add 'material' property to one specific ply. The logic/philosophy here is that the smallest object always superceeds the 
properties in parent object, if same property is specified under both.



Spline Generation
-----------------

Standard is designed to work with multiple different software that generate or export splines, some of which do not provide information on how splines are generated mathematically. 
Therefore the practical approach is to increase number of points stored in order to provide more precise spline for delimiation. This is currently considered sufficient for all 
forseen applications. 

Some delimations, however, will require spline breaks. Those can be specified by ``breaks`` parameter in :func:`CompositeStandard.Spline`. The most common purpose for these are part/ply corners.
These should help wherever the used software struggles to provide reasonable continuity betwen points.