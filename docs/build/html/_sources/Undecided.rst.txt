Undecided
=========

This section outlines objects that are being considered, but are currently not part of the core :func:`CompositeStandard`.

Opinions/preferences regarding all below are very welcome by the authors.

Zones
-----

Everyone might have slightly different definition of zones, with different purpose. Here we are talking of anything that benefits of specific definition of area that certain definition relies on. 
Most composite information can be stored in current version of CompoST, but in some cases it might not be the most practical. For instance one might want to apply a tolerance over an area, that does not correspond to full plies,
but rather to certain critical part of component, regardless ply limits. The same zone might than be used in FE to define more dense mesh. Each of these are currenlty supported by CompoST, but if the same zone is used for multiple
purposes it is not immediatly clear. In such cases zones would be useful.

However, author refrains from specifying what exactly would 'Zone' object look like until few use-cases that require 'Zone' are available and can be studied. 

Features
--------

Features are engineering objects that have their special purpose/rules in engineering workflow, but are not directly defined as either composite or STEP object. These include for example: fillets, chamfers, holes, tool radii...

These are currently considred as out of scope for CompoST. The reason is that features are consdiered post-procesing of STEP format in most cases, while CompoST is only supposed to include geometric definition
required for definition of composite objects. However, authors are considring enabling "Feature" objects in some format to essentially allow for flexible appendage to the CompoST file.