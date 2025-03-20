# To bind or not to bind? Replaying object-centric processes under stable relationships

This repository contains:
- the [extended version](extended_paper.pdf) of the paper including the detailed proof of our theorems in the appendix,
- the [python script](myOCELinspector.py) based on [pm4py](https://pypi.org/project/pm4py/) to inspect the object type relaionships of [benchmark OCELs](https://www.ocel-standard.org/event-logs/overview/),
- and the [results](result.txt) of running the script for the OCELs for Logistcs, Order Management, Procure-to-Pay, LRMS, Hinge Production, and Age of Empires.

## Inspection results

The results of our analysis are displayed in the following table. For each analyzed OCEL, it holds the number of object types, and the number of bidirectional relationships between object types. The relationships can be of three different types: many-to-many, many-to-one, and one-to-one. In the paper, we define stable m2o relationships. As elaborated, a many-to-one relationship manifests as one stable m2o relationship in our approach, while a bi-directional one-to-one relationship manifests two stable m2o relationships.

For every OCEL, we calculate the number of stable many-to-one relationships (m2o) with a filtered noise threshold of 0.1, and 0.0 (no filter). The number of stable m2o relationships combines all many-to-one relationships, and double the number of the bi-directional one-to-one relationships.

For instance, the LRMS-O2C log with noise 0.1 holds, in total, 11 relationships, with 1 many-to-many, 2 many-to-one, and 8 one-to-one relationships. Hence, we add up to 2 + 2*8 = 18 stable m2o relationships.

<img src="table.png" alt="drawing" width="800"/>
