================================
Welcome to the project "cc-dcr"
================================
This project is a result of the research process beneath a Master's thesis.
It is concerned with the development of a conformance checking tool for `DCR graphs <http://wiki.dcrgraphs.net/>`_.
Please note, that the core code of the repository is in the folder *'./cc-dcr'*.

Getting started
==================
| To get started with conformance checking the prerequisite needs to be satisfied.
| Additionally, you need to install the project dependencies


###################
Prerequisites
###################
The tool requires the installation of at least ``Python 3.6`` or on Windows ``Anaconda 3``

###################
Installation
###################

In order to execute the "cc-dcr.py" the installation of the packages in the requirements.txt are necessary:

- Therefore, you can call the makefile with:

    ``"make init"``

- Otherwise, you can execute the command:

    ``"pip install -r requirements.txt"``

###################
Running the tests
###################
The project currently contains two separate test suites:

1. Micro Tests

    - These tests are used to check the micro functionality of each class
    - They do not import an event log but work with controlled conditions
    - The tests sources can be found directly in ``./tests``.
    - To execute the tests you can use either the makefile if you are operating on a UNIX based OS
    - Or you can simply call the tests with python -m unittest [testModule]. For example:

        - ``python -m unittest tests.test_marking``
        - Note that, your terminal must be in the project root folder

2. Evaluation Tests (Integration Tests)

    - These tests are used to validate the behavior of the tool
    - In these tests event logs are imported and used
    - The tests sources can be found directly in ``./tests/Evaluation``.
    - Executing these tests is done by calling the script frq_evaluator.py
    - Usage:

        1. ``cd tests\Evaluation``

        2. ``python frq_evaluator.py``
        - Note that you must be in the Evaluation folder to make the script work

*******************
Micro-Tests
*******************
There are currently four unittest modules for the micro tests

test_conn.py
---------------
- These tests are concerned with DCR graphs `relations <http://wiki.dcrgraphs.net/wiki/9/connection>`_.
- Their main purpose is to check if transitions and constraints are parsed and interpreted correcty

test_marking.py
-----------------
- These tests are concerned with DCR graphs markings.
- Their purpose is to guarantee the correct behaviour for a present marking when performing transitions in markings

test_graph.py
---------------
- These tests are used to check if the parsing of a DCR graph from an XML file works properly

test_eventlog_parser.py
------------------------
- These tests are used to check if the parsing of an event log works as expected

***********************
Evaluation Tests
***********************
These tests were initially implemented to prove that the conformance checking algorithm works as it should. The output
of the conformance checking tool is assessed at the end therefore these tests represent so-called end to end tests.

test_frq1evaluation.py
------------------------
In a DCR graphs process model roles can be assigned to activities. The tests in this file prove that the conformance
checking tool detects events which were executed by a non-assigned role.

test_frq2evaluation.py
------------------------
In a DCR graphs process model activities can be excluded from their execution. These tests prove that the infringed
activities can be retrieved as expected.

test_frq3evaluation.py
------------------------
In a DCR graphs process model activities may not be pending for execution at the end of a process trace. These tests
prove that the violation of the pending constraint can be checked.

test_frq4evaluation.py
------------------------
DCR graphs can do transitions in the marking of a process model. The relations Include, Exclude and PendingResponse cause
these transitions. The tests in this module check if the conduction of the transitions is correctly done or not.

test_frq5evaluation.py
------------------------
DCR graphs have a relation type called Condition. The target activity of a Condition connection may only be executing
when the source activity has either been executed yet or is currently excluded from the graph. These tests prove if
violations of the Condition constraint can be identified correctly

test_frq6evaluation.py
------------------------
DCR graphs have a relation type called Milestone. The target activity can  occur as long as the source activity is
not included an pending at the same point of time

.. _frq7:

test_frq7evaluation.py
------------------------
DCR graphs relations can be augmented by so-called Guards. Guards are boolean expressions "``(data < 100)``" that refer
to data in an event log. If the data in the event evaluates the expression to true, a relation is active.
This test module proves that the tool retrieves data correctly from an event log and also evaluates expressions correctly

These tests especially focus on the data that occurs in the source event of an activity

test_frq8evaluation.py
------------------------
DCR graphs can contain so-called nesting activities, these activities contain other activities. If a nesting activity
is the target of a relation all activities nested under the nesting activity are affected by the relation. If the nesting
activity is the source of a transition relation the transition always triggers when a nested event occurs.
Furthermore the transition of the marking behaves a little different for nesting activities.

The tests in this test module are used to prove the correctness of the tool's behavior regarding nesting activities

test_frq9evaluation.py
------------------------
These tests extend the tests of frq7_ to check constraints like "``(a.data > 10)``", so that the prefix a can be related
to the correlated event a in an event log
These tests prove the functionality to handle these kinds of expressions


##################
Running the tool
##################

To run the actual conformance checking the module cc_dcr.py in the package "conformancechecker". To provide
the resources you have two options:

1.  Simply call the module via command line
2.  Change the default values in the ``cmd_parser.py`` module

*******************
Command line args
*******************

| ``cd conformancechecker``
| ``cc_dcr.py [--eventLog example_log.xes] [--XmlDcr example_graph.xml] [--use_celonis]``

--eventLog      Path of the event log that should be checked
--XmlDcr        Path of the DCR graphs process model
--use_celonis   Sets the flag if celonis import is used to retrieve an event log


*******************
Default args
*******************
If you want, you can also adjust the default command line values. Therefore, you need to change the tags
``default=`` tags in the file ``cmd_parser.py``

##################
Contributing
##################
First, to open to the code documentation in ``./docs``use the provided sphinx makefile or make.bat with the target
``html`` to build the documentation. Note that, you have to install the requirements before.

    1. ``cd .\docs``
    2. ``make html``

Afterward, the folder ``.\docs\_build\html`` is built. Here, there is now a file called ``index.html`` which contains
the summary of all Inline code documentation with descriptions.

Second, you can enhance the sources in the package ``.\conformancechecker``.

Third, feel free to add some more tests in the ``.\tests`` package, for either already existing module to get an understanding
for the exiting tool or for the new functions that you added.

###################
Authors
###################
- **Sebastian Dunzer**, *Initial work*


####################
License
####################
This project is currently Licensed under the MIT-License - see `License <LICENSE>`_ for more information
