import math
import pm4py
from pm4py.ocel import ocel_get_object_types, ocel_object_type_activities
from pm4py import ocel_objects_interactions_summary, ocel_objects_summary
import sys
import numpy
from functools import reduce

BAR = "================================================================================"

def import_ocel(filename):
  #print("Import started")
  if "xml" in filename:
    ocel = pm4py.read_ocel2_xml(filename)
  elif "json" in filename:
    ocel = pm4py.read_ocel2_json(filename)
  else:
    raise Exception("Unexpected file format, expected .xml or .json")
  #print("Import done")
  sys.stdout.flush()
  return ocel

def get_object_type_dict(ocel, object_types):
  types_of_objects = {}
  myobjects  = ocel.objects.reset_index() 
  for index, row in myobjects.iterrows():
    types_of_objects[row["ocel:oid"]] = row["ocel:type"]
  return types_of_objects

def object_relationships(object_summary, types_of_objects, object_types):
  distinct_object_types = [tuple([t1,t2]) \
    for t1 in object_types for t2 in object_types if t1 != t2]
  relationships = dict([ (ts, []) for ts in distinct_object_types ])
  # walk over objects
  partners = {}
  object_summary  = object_summary.reset_index() 
  for _, row in object_summary.iterrows():
    oid = row["ocel:oid"]
    otype = types_of_objects[oid]
    partners[oid] = row["interacting_objects"]
    interacting_types = [ types_of_objects[pid] for pid in partners[oid]]
    for mtype in object_types:
      mobjects = [ x for x in partners[oid] if types_of_objects[x] == mtype]
      num_m_partners = len(mobjects)
      if otype != mtype:
        key = tuple([otype,mtype])
        relationships[key].append(num_m_partners)
  return relationships

def classify_relationships(relationships):
  to_one = []
  to_almost_one = []
  to_many = []

  print("INTERACTION COUNTS")
  for ((otype,mtype), counts) in relationships.items():
    if len(counts) > 0:
      ratio = float(sum(counts)) / len(counts)
      cmax = max(counts)
      cmin = min(counts)
      if cmax == 0:
        continue # no interactions at all, so we ignore this relationship
      print("A %s interacts with [%d, %d] %s (on average %.3f)." % (otype, cmin, cmax, mtype, ratio))
      if ratio == 1.0:
        to_one.append(tuple([otype,mtype]))
      elif ratio > 1.0 and ratio <= 1.05:
        to_almost_one.append(tuple([otype,mtype]))
      else:
        to_many.append(tuple([otype,mtype]))
  print("")
  return to_one, to_almost_one, to_many

def classify_relationship_pairs(to_one, to_almost_one, to_many):
  distinct_object_types = [tuple([t1,t2]) \
    for t1 in object_types for t2 in object_types if t1 != t2]
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
  print("")

def check_consistent_object_types_of_event_types(ocel, object_types, object_type_dict):
  event_types = {}
  event_count = {}
  for _, r in ocel.get_extended_table().iterrows():
    rd = r.to_dict()
    event_type = rd["ocel:activity"]
    event_count[event_type] = event_count[event_type]+1 if event_type in event_count else 1
    interacting_types = set()
    for t in object_types:
      if isinstance(rd["ocel:type:"+t], list):
        interacting_types.add(t)
    #if event_type == "Load to Vehicle":
    #  print(rd)
    #  break
    itypes_key = frozenset(interacting_types)
    if not event_type in event_types:
      event_types[event_type] = { itypes_key: 1}
      #if event_type == "build":
      #  print("Event type %s has interacting types: %s" % (event_type, interacting_types))
    else:
      #if event_type == "build":
      #  if itypes_key not in event_types[event_type]:
      #    print("Event type %s has  interacting types: %s " % (event_type, interacting_types))
      #    print(rd.items())
      if itypes_key in event_types[event_type]:
        event_types[event_type][itypes_key] += 1
      else:
        event_types[event_type][itypes_key] = 1

  print("OPTIONAL OBJECT TYPES IN EVENTS")
  for e, types in event_types.items():
    if len(types) == 1:
      print("Event type %s has no optional types." % e)
    else:
      ts_opt = [o for o in object_types if any([o not in ts for ts in types]) \
            and any([o in ts for ts in types])]
      ts_opt_cnt = [ (t, sum([ c for (ts, c) in types.items() if t not in ts])) for t in ts_opt ]
      ts_opt_str = ["%s missing in %d events," % (t,c) for t,c in ts_opt_cnt]
      print("Event type %s has optional types:" % e, *ts_opt_str, "of %s events in total" % event_count[e])

if __name__ == "__main__":
  ocel = import_ocel(sys.argv[1])

  print(BAR, "\n", sys.argv[1])
  print(BAR)
  object_types = ocel_get_object_types(ocel)
  print("OBJECT TYPES")
  print(object_types, "\n")
  object_summary = ocel_objects_summary(ocel)
  for col in ['activities_lifecycle', 'lifecycle_start', 'lifecycle_end', 'lifecycle_duration']:
    object_summary = object_summary.drop(col, axis=1)

  # determine object types
  types_of_objects = get_object_type_dict(ocel, object_types)

  # determine relationships
  relationships = object_relationships(object_summary, types_of_objects, object_types)
  
  # classify relationships
  to_one, to_almost_one, to_many = classify_relationships(relationships)

  # classify relationship pairs
  classify_relationship_pairs(to_one, to_almost_one, to_many)

  check_consistent_object_types_of_event_types(ocel, object_types, types_of_objects)

