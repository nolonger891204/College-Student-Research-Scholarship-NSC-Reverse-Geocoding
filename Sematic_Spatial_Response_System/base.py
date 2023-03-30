# convert geojosn to wkt and get its geom type
def geojsonToWKT(geojson_object):
  json_object = geojson_object["features"][0]["geometry"]
  geom_type = geojson_object["features"][0]["geometry"]["type"]
  from shapely.geometry import shape
  geom = shape(json_object)
  return (geom.wkt, geom_type)

# covert response string to json object
def csvStringToJsonObject(response_string):
  import csv, io, json
  reader = csv.DictReader(io.StringIO((response_string)))
  json_data = json.dumps(list(reader))
  json_data = json.loads(json_data)
  return json_data

# covert some string 
def getClassandFromIri(old_str):
  new_str = old_str.replace("http://www.semanticweb.org/win/ontologies/2023/1/disaster#", "")
  return new_str

def getNameFromOntoClass(old_str):
  new_str = str(old_str).replace("dis_0223.", "")
  return new_str