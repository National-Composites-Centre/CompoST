Development
===========

(Under Development)

The general development of CompoST until 1.0 focuses mainly on standardising all objects that are critical for most composite related operations, at any stage of design or manufacture. 

Until 1.0 most use-cases will be internal, as that way any interative changes to the core CompoST objects will not negatively impact any collaborations. However, further the CompoST development should be based
on industrial and academic use-cases. These should only minimally affect core CompoST definitions. However, some editing (versioning) of the core CompoST must be assumed, to accomodate for cases that have not yet been
considered. Overall, most code developed for individual use cases should ideally be stored in https://github.com/National-Composites-Centre/CST_utils , or in specific dedicated repository, for re-usability and community 
visibility. 

Once use-cases for majority of applications have been demonstrated, only minimal edits to core CompoST should be done. Process of approvals and evaluation of effects will be developed at this stage. However, everyone is always
free to clone core CompoST and modify it locally for their purposes. The only downside of this is will be that the community developed script might not function of the shelf as intended.

Unit Testing
------------

Unit testing enables development of CompoST without affecting built in core utility functions.

This will be expanded as the functionality expands. Each utility function should have dedicated test function in 'Tests\test_main.py', this function is then called from 'TestMainCompoST'.
To run the tests the following command should be used in the root CompoST directory:

.. code-block:: bash

	python -m unittest discover -s tests

The following function creates a dedicated example CompoST. This object contains various different ways to store information. For example, 'CompositeStandard.Piece' is stored as part of a 'CompositeStandard.Ply', as well as part of 'CompositeStandard.Sequence', and as well as within the overarching 'allComposites' list.

.. py:function:: create_example()

This following function is used to check that re-linking of objects after deserialization works, i.e. objects with same ID continue to be treated as one object and it's life copies.

.. py:function:: testReLink(CompoST)

The following function is very simple test that verifies that the expected number of objects are contained in the root lists ('allComposites','allGeometry',...)

.. py:function:: NewFileComparison(CompoST)


Use Cases
---------

Use cases can be only simple data input/export tasks, or full blown detailed processes including many steps. In either case, an existent proces is identified and CompoST is implemented as the main storage mechanism for composite
data. If any developments are required, these are done and recoreded CST_utils repository, or directly in CompoST if these solve core requirements.

(include use case pages here -- as a new tree)
(add use case page template)


Collaborations
--------------

Collaborations will mainly be required where export/import from a software is required. This can sometimes be developed on software user (our) side. However, very often the APIs of the software do not support the level of scripting
required to develop CompoST integration tools. In such cases key collaborations will be identified. The funding of the collaborative development will depend on the use-case. 

(include collaboration pages here -- these might only be publishable following the succesful collaboration)
(add colaboration page template )


Versions tracking
-----------------
The vesion system uses standar python approch consisting of 3 numbers e.g. 1.2.3, major.minor.patch.

Before pushing/merging to main the appropriate command from the below has to be run.

.. code-block:: bash

	bump2version.exe bumpversion patch
	
	bump2version.exe bumpversion minor
	
	bump2version.exe bumpversion major
	
Tags should be pushed as follows

.. code-block:: bash

	git push origin branch_name --tags 