IDs
===

Every object belonging to :py:meth:`~CompositeStandard.CompositeDBItem.get` family can have 'ID' parameter attributed to it. This allows for referencing geometries and composite elements without re-creating them. The most common usage of this is when 'CompositeStandard.Piece' uses parameter splineRelimitation to signifcy edge of the composite piece, this parameter is simply and integer - 'ID', and corresponding spline can be found in GeometricElement`


IDs are not compulsory for any object, but it is highly recommended that most objects are given IDs, as that will facilitaty any re-use. Exceptions are objects that will definitely not see reuse, such as point only existing to create a complex spline.


