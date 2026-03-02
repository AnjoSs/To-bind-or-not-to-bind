# To bind or not to bind? The Assumption of Stable Relationships in Object-centric Process Mining

This repository contains the supplementary material to two papers:
   * "To bind or not to bind? Replaying object-centric processes under stable relationships" in [this branch](https://github.com/AnjoSs/To-bind-or-not-to-bind/tree/er-2025).
   * "The Assumption of Stable Relationships in Object-centric Process Mining" in the current branch.

In this repository, you can find:
1. An inspection of object type relationships in existing benchmark OCELs:
    * The [python script](src/ocel_inspector.py) based on [pm4py](https://pypi.org/project/pm4py/) counts the object relationships of [benchmark OCELs](https://www.ocel-standard.org/event-logs/overview/).
    *  The [results](results/result.txt) reports on the results obtained by this script for the OCELs for Logistics, Order Management, Procure-to-Pay, the LRMS collection, Hinge Production, Age of Empires, Bundesttag, Angular GitHub Commits, and Inventory Management.
3. An implementation of our mapping from OCPN to OPID (The original repository is available [here](https://github.com/bytekid/ocpn2opid)):
    * The [python script](src/ocpn2opid.py) implements the mappings presented in the paper.
    * The [examples directory](examples) provides a set of [sample OCPNs](https://github.com/rwth-pads/ocpn-visualizer/tree/master/public/sample_ocpns/json) and the mapped OPIDs (summarized in the table below).

## 1. Object relationships in OCELs

Our analysis of the [benchmark OCELs](https://www.ocel-standard.org/event-logs/overview/) iterates all objects in the log. For each object and possibly related object type, it counts to how many objects are corelated in any event. For every possible pair of object types, this results in a set of relationships, with an interval representing the multiplicities for each side of the relationship. For each OCEL, we report the resulting relationships in a separate file in the [results folder](results).

The results of our analysis are displayed in the following table. For each analyzed OCEL, it holds the number of object types, and the number of bidirectional relationships between object types. It displays the amount of stable many-to-one relationships with the multiplicities 1..*-1..1, 0..*-1..1, 1..*-0..1, and 0..*-0..1, and amount of stable one-to-one relationships of the types 1..1-1..1, 0..1-1..1, and 0..1-0..1. Finally, this results in a number of functional dependencies for each log.

<img width="955" height="476" alt="image" src="https://github.com/user-attachments/assets/8b00eacc-4e0e-406b-b922-855d389db197" />

Additionally, for every OCEL and any event type, the according events are iterated to check the set of object types that an event type operates on. If events of the same event type appear with different sets of object types, then there are optional object types for one event type. For example, in the AoE log, we find:
```
Event type Start Build Barracks has optional types: Villager missing in 53 events, of 4057 events in total
```
For the event type `Start Build Barracks`, we can find 53 events, in which the processed objects contain no `Villager`. In all other 4004 events, a villager is processed.
  
## 2. Prototypical implementation of the Mapping

### Implementation script

The Python command line script can be called as
```sh
 $ python3 ocpn2opid.py examples/Recruiting/ocpn.json 
 $ python3 ocpn2opid.py -R "[(offers:applications)]" examples/Recruiting/ocpn.json 
```

It takes an OCPN in [json format](https://github.com/rwth-pads/ocpn-visualizer/) as input, and produces a pnml file out.pnml and a .dot visualization of the resulting OPID in out.dot.
The `-R` parameter is optional: if it is omitted, only transformation T1 is applied. Otherwise, -R should be followed by a list of pairs of object types that should be considered many-to-one relationships, in a format such as `[(many1:one1),(many2:one2),(many3:one3)]`.


### Evaluation Script

We applied our script to the sample OCPNs in [this repository](https://github.com/rwth-pads/ocpn-visualizer/), excluding nets that have only one object type or are otherwise syntactic. The following table summarizes the results.
The Python command-line script can be obtained [here](code.zip) to reproduce the results.


|     |     |     |     |
| --- | --- | --- | --- |
| **OCPN** | **OPID N1** | **many-to-one relations** | **OPID N2** |
| [Applications and offers](./examples/Applications_and_offers/ocpn.json) | [pnml](./examples/Applications_and_offers/N1.pnml), [png](./examples/Applications_and_offers/N1.png), [pdf](./examples/Applications_and_offers/N1.pdf) | \[(offer:application)\] | [pnml](./examples/Applications_and_offers/N2.pnml), [png](./examples/Applications_and_offers/N2.png), [pdf](./examples/Applications_and_offers/N2.pdf) |
| [Cyclic OCPN](./examples/Cyclic_OCPN/ocpn.json) | [pnml](./examples/Cyclic_OCPN/N1.pnml), [png](./examples/Cyclic_OCPN/N1.png), [pdf](./examples/Cyclic_OCPN/N1.pdf) | \[(item:order)\] | [pnml](./examples/Cyclic_OCPN/N2.pnml), [png](./examples/Cyclic_OCPN/N2.png), [pdf](./examples/Cyclic_OCPN/N2.pdf) |
| [Exported P2P](./examples/Exported_P2P/ocpn.json) | [pnml](./examples/Exported_P2P/N1.pnml), [png](./examples/Exported_P2P/N1.png), [pdf](./examples/Exported_P2P/N1.pdf) | \[(MATERIAL:PURCHREQ),(MATERIAL:PURCHORD)\] | [pnml](./examples/Exported_P2P/N2.pnml), [png](./examples/Exported_P2P/N2.png), [pdf](./examples/Exported_P2P/N2.pdf) |
| [Kolloquium example](./examples/Kolloquium_example/ocpn.json) | [pnml](./examples/Kolloquium_example/N1.pnml), [png](./examples/Kolloquium_example/N1.png), [pdf](./examples/Kolloquium_example/N1.pdf) | \[(turq:yel),(yel:turq)\] | [pnml](./examples/Kolloquium_example/N2.pnml), [png](./examples/Kolloquium_example/N2.png), [pdf](./examples/Kolloquium_example/N2.pdf) |
| [OCPA P2P](./examples/OCPA_P2P/ocpn.json) | [pnml](./examples/OCPA_P2P/N1.pnml), [png](./examples/OCPA_P2P/N1.png), [pdf](./examples/OCPA_P2P/N1.pdf) | \[(item:order)\] | [pnml](./examples/OCPA_P2P/N2.pnml), [png](./examples/OCPA_P2P/N2.png), [pdf](./examples/OCPA_P2P/N2.pdf) |
| [Order Process](./examples/Order_Process/ocpn.json) | [pnml](./examples/Order_Process/N1.pnml), [png](./examples/Order_Process/N1.png), [pdf](./examples/Order_Process/N1.pdf) | \[(item:order)\] | [pnml](./examples/Order_Process/N2.pnml), [png](./examples/Order_Process/N2.png), [pdf](./examples/Order_Process/N2.pdf) |
| [Recruiting](./examples/Recruiting/ocpn.json) | [pnml](./examples/Recruiting/N1.pnml), [png](./examples/Recruiting/N1.png), [pdf](./examples/Recruiting/N1.pdf) | \[(offers:applications)\] | [pnml](./examples/Recruiting/N2.pnml), [png](./examples/Recruiting/N2.png), [pdf](./examples/Recruiting/N2.pdf) |
| [Syntactic cyclic OCPN](./examples/Syntactic_cyclic_OCPN/ocpn.json) | [pnml](./examples/Syntactic_cyclic_OCPN/N1.pnml), [png](./examples/Syntactic_cyclic_OCPN/N1.png), [pdf](./examples/Syntactic_cyclic_OCPN/N1.pdf) |     | [pnml](./examples/Syntactic_cyclic_OCPN/N2.pnml), [png](./examples/Syntactic_cyclic_OCPN/N2.png), [pdf](./examples/Syntactic_cyclic_OCPN/N2.pdf) |
| [Simple example with cycle](./examples/Simple_example_with_cycle/ocpn.json) | [pnml](./examples/Simple_example_with_cycle/N1.pnml), [png](./examples/Simple_example_with_cycle/N1.png), [pdf](./examples/Simple_example_with_cycle/N1.pdf) |     | [pnml](./examples/Simple_example_with_cycle/N2.pnml), [png](./examples/Simple_example_with_cycle/N2.png), [pdf](./examples/Simple_example_with_cycle/N2.pdf) |


