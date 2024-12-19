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


Active object
-------------

Most objects contain ``active``  property. This is used for cases when data needs to be kept, but is superceeded. For example, if wrinkle has been identified in a scan, the detail of the wrinkle is stored. However, user might then
implement a process for removing that wrinkle, either eradicating it or replacing it by wrinkle with new data. In this case the property ``active`` will be switched from 'True' to 'False'. When this property is not used, user should
assume the object is active. This needs to be kept in mind in processes where some objects might be de-activated, as any furhter processing/analysis will need to exclude based on this property/tag.

.. _stages-reference:

Stages
------

Stages help with tracking information sources, allowing for history of changes to the part. Each object can have reference so stages (`Stage` object) to indicate when and how was this object edited.

On default if `Stage` is not assigned to an object it should be assumed this object was last edited during the component design stage.

Stages should all be stored in `allStages` list for iteration. When new stage is created the `StageID` should be selected to be +1 to the highest number currently listed. 

There are two suggested workflows for working with stages. First option is to pre-define all stages at design, assuming the designer knows all the processes that will utilize CompoST in the design, manufacture, and potentially lifecycle of the product.
In this case the `Stage` objects are already all stored, and at each stage new objects are simply created with appropriate ID. For second method the `allStages` list is left empty at design stage, and each stage is created when the data is being stored.
Which option is selected will depend on where in the design process decisions are being made about the product. The first option allows the `allStages` to also be a workflow definition, with majority of the information being stored in process documents 
referenced in individual stages. The second option allows for more flexibility.

When an object is invalidated by a new stage, the old object's `active` property should be changed to `False` (it is `True` on default). The example of this is a Wrinkle found in a ply, that was fixed by subsequent operation. In this case it may be desirable 
to keep the Wrinkle stored for traceability, to to de-activate the object to indicate it no longer affects the part.

To define `Stage` the default object `Stage` can be used, with majority  of information being stored in reference documents. However, it is assumed that companies might want to create specific `Stage` objects that can then be reused for multiple parts.
These bespoke objects should be stored in local version of `CompositeStandard`. 

Edge of Part
------------

On default all composite objects are defined with the "manufacturing edge of ply". The 'EngEdgeofPart' simulates the final trimming operation, and simply relimits the part according to final trimming operation.

(This logic can still be modified based on real examples and induced limitations)