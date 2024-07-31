IDs
===

Every object belonging to :py:meth:`~CompositeStandard.CompositeElement.get` or :py:meth:`CompositeStandard.GeometricElement` can have 'ID' parameter attributed to it. This allows for referencing geometries and composite elements without re-creating them. The most common usage of this is when 'CompositeStandard.Piece' uses parameter splineRelimitation to signifcy edge of the composite piece, this parameter is simply and integer - 'ID', and corresponding spline can be found in GeometricElement`

