import pm4py
from pm4py.ocel import ocel_get_object_types, ocel_object_type_activities
from pm4py import ocel_objects_interactions_summary, ocel_objects_summary
import sys
from functools import reduce



filename = sys.argv[1]
print("Import started")
ocel = pm4py.read_ocel2_xml(filename)
print("Import done")
sys.stdout.flush()

object_types = ocel_get_object_types(ocel)
print("object types")
print(object_types)
object_summary = ocel_objects_summary(ocel)
for col in ['activities_lifecycle', 'lifecycle_start', 'lifecycle_end', 'lifecycle_duration']:
  object_summary = object_summary.drop(col, axis=1)
# print(object_summary.head(10))

# determine object types
types_of_objects = {}
myobjects  = ocel.objects.reset_index() 
for index, row in myobjects.iterrows():
  types_of_objects[row["ocel:oid"]] = row["ocel:type"]
#print(types_of_objects)

distinct_object_types = [tuple([t1,t2]) \
  for t1 in object_types for t2 in object_types if t1 != t2]

relationships = dict([ (ts, []) for ts in distinct_object_types ])
# walk over objects
partners = {}
object_summary  = object_summary.reset_index() 
for index, row in object_summary.iterrows():
  oid = row["ocel:oid"]
  otype = types_of_objects[oid]
  partners[oid] = row["interacting_objects"]
  interacting_types = [ types_of_objects[pid] for pid in partners[oid]]
  for mtype in set(interacting_types):
    mobjects = [ x for x in partners[oid] if types_of_objects[x] == mtype]
    num_m_partners = len(mobjects)
    if otype != mtype:
      key = tuple([otype,mtype])
      relationships[key].append(num_m_partners)

to_one = []
to_almost_one = []
to_many = []

print("PRECISE COUNTS")
for ((otype,mtype), counts) in relationships.items():
  if len(counts) > 0:
    ratio = float(sum(counts)) / len(counts)
    print("A %s interacts on average with %.3f %s." % (otype, ratio, mtype))
    if ratio == 1.0:
      to_one.append(tuple([otype,mtype]))
    elif ratio > 1.0 and ratio <= 1.05:
      to_almost_one.append(tuple([otype,mtype]))
    else:
      to_many.append(tuple([otype,mtype]))
print("")

rel_kinds = {"one2one": [], "one2almostone": [],"almostone2almostone": [],"many2one": [], "many2almostone": [], "many2many": []}
for type_pair in distinct_object_types:
  (type1, type2) = type_pair
  if type1 < type2:
    continue # just to process every pair only once
  rtype_pair = tuple([type2, type1])
  if type_pair in to_one and rtype_pair in to_one:
    rel_kinds["one2one"].append(type_pair)
  elif type_pair in to_one and rtype_pair in to_almost_one:
    rel_kinds["one2almostone"].append(rtype_pair)
  elif rtype_pair in to_one and type_pair in to_almost_one:
    rel_kinds["one2almostone"].append(type_pair)
  elif rtype_pair in to_almost_one and type_pair in to_almost_one:
    rel_kinds["almostone2almostone"].append(type_pair)
  elif type_pair in to_one and rtype_pair in to_many:
    rel_kinds["many2one"].append(type_pair)
  elif rtype_pair in to_one and type_pair in to_many:
    rel_kinds["many2one"].append(rtype_pair)
  elif type_pair in to_almost_one and rtype_pair in to_many:
    rel_kinds["many2almostone"].append(type_pair)
  elif rtype_pair in to_almost_one and type_pair in to_many:
    rel_kinds["many2almostone"].append(rtype_pair)
  else:
    rel_kinds["many2many"].append(type_pair)

print("RELATIONSHIP TYPES")
for (kind, type_pairs) in rel_kinds.items():
  if len(type_pairs) == 0:
    continue
  ls = reduce(lambda acc, ts: "(%s, %s), %s" % (ts[0], ts[1], acc), type_pairs, "")
  print("%d %s: %s" % (len(type_pairs), kind, ls))



#print("%d types, %d one2one, %d many2one rigid, %d many-to-one non-rigid, %.1f many2many" % (len(object_types), kinds[0], kinds[1], mtmnr, kinds[2]))