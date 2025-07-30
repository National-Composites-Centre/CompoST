Versions
========
This section exists mainly for traceability. It may also allwo users to work with older versions of CompoST if specific
development conflicts with their workflow.

Note: if you are not using the latest version, you may be able to access older (more appropriate docs) in "OlderVersionDocs" directory in gh-pages branch.

Before 1.0 this list of changes will not be exhaustive, only major changes for reference will be tracked here.

0.71a
-----
The main developments of 0.71 are the edge-of-ply tolerenaces and defects, along with corresponding edge-of-part definition.

This version also allow for explicitely stating the status of defect, to help distinuguish between simple variation measurments and defect
that does not fit within tolerance.

Unified 'SplineRelimitation' objects - now they are available both as object and integer for all 'CompositeElement' objects.

Removed obsolete 'map' parameter from 'Defect'.

0.7.3
-----

PEP following version system using bumpversion.
Effective properties introduced.

0.7.4
-----

pip installation from GitHub enabled.


0.8.0
-----

Contains initial object for simulations
Save and Load functions available in the main 'CompositeStandard' file.

0.8.2
-----

Initial unit-test functions implemented.
Re-link improved, now reliable for mixture of lists and objects in tree.

0.9.0
-----

The core aspect of this version is to enable storage of information regarding filament winding processes. This should be done in a way that furhter manufacturing processes can be added with lesser distruptions.

Since this results in some changes to existent classess, it is good time to clean up existent objects and remove any parameters that seemed unnecessary in retro-spective, such us splineRelimitationRef - with the automated re-linking feature there 
is almost never benefit to this methodology as compared to direclyt referencing the spline under 'splineRelimitation', which stores copy of the object.

0.9 is unlikely to be compatible with 0.8 files, use if no legacy files are used in project.