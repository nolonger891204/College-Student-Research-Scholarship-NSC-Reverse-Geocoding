USER = ''
PASSWORD = ''

# sparql prefix
sparql_prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\
  PREFIX : <http://www.semanticweb.org/win/ontologies/2023/1/disaster#>\
  PREFIX geo: <http://www.opengis.net/ont/geosparql#>\
  PREFIX geof: <http://www.opengis.net/def/function/geosparql/>\
  PREFIX  ngeo:<http://geovocab.org/geometry#>\
  PREFIX  gn: <http://www.geonames.org/ontology#>\
  PREFIX  foaf:<http://xmlns.com/foaf/0.1/>\
  PREFIX uom: <http://www.opengis.net/def/uom/OGC/1.0/>"\

# get basic sparql (equal)
def returnBasicSparql(geom_type, spatial_relation, wkt):
  return sparql_prefix + "select ?class ?name where { \
    VALUES ?class {" + geom_type + "}.\
    ?id a ?class.\
    ?id geo:hasGeometry ?geo.\
    ?geo geo:asWKT ?wkt.\
    ?id foaf:name ?name.\
    FILTER( "+ spatial_relation +"(?wkt,'''\
        <http://www.opengis.net/def/crs/OGC/1.3/CRS84>" + wkt + "'''^^geo:wktLiteral))}"

# get basic sparql (equal)
def returnBasicSparqlTESTING(geom_type, spatial_relation, wkt_query):
  return sparql_prefix + "select ?class ?name where { \
    VALUES ?class {" + geom_type + "}.\
    ?entity a ?class;\
      geo:hasGeometry ?geom;\
      foaf:name ?name.\
    ?geom geo:asWKT ?wkt.\
    ?pbarea a :PublishArea;\
      geo:asWKT ?fwkt.\
    FILTER(STR(?pbarea) = '" + wkt_query + "')\
    FILTER( "+ spatial_relation +"(?wkt, ?fwkt))}"

# get intersect sparql (SPEED UP!!!)
def returnLimitSparq(geom_type, spatial_relation, wkt_query, some_limit, limit_col):
  return sparql_prefix + "select ?class ?name where { \
    VALUES ?class {" + geom_type + "}.\
    VALUES ?lname {" + some_limit + "}.\
    ?entity a ?class;\
      geo:hasGeometry ?geom; "+ limit_col +" ?lname; foaf:name ?name.\
    ?geom geo:asWKT ?wkt.\
    ?pbarea a :PublishArea;\
      geo:asWKT ?fwkt.\
    FILTER(STR(?pbarea) = '" + wkt_query + "')\
    FILTER("+ spatial_relation +"(?wkt, ?fwkt))}"

# get distance sparql
def returnSparqlDistance(geom_type, distance, wkt_query):
  sname_selector = ""
  sname_query = ""
  if ( geom_type == ":Road" ):
    sname_selector = "?sname "
    sname_query = ":roadsectionname ?sname;"
    
  return sparql_prefix + "select ?class ?name "+ sname_selector +"?dist where { \
    VALUES ?class {" + geom_type + "}.\
    ?entity a ?class;\
      geo:hasGeometry ?geom; "+ sname_query +" foaf:name ?name.\
    ?geom geo:asWKT ?wkt.\
    ?pbarea a :PublishArea;\
      geo:asWKT ?fwkt.\
    FILTER(STR(?pbarea) = '" + wkt_query + "')\
    BIND(geof:distance(?wkt, ?fwkt, uom:metre) as ?dist)\
    FILTER(?dist<"+ str(distance) +")}\
    GROUP BY ?class ?name ?dist"+ sname_selector +" ORDER BY ASC(?dist) \
    limit 10"

# get buffer and intersect sparql
def returnSparqlBuffer(geom_type, spatial_relation, radius, wkt_query):
    return sparql_prefix + "select ?class ?name where { \
    VALUES ?class {" + geom_type + "}.\
    ?entity a ?class;\
      geo:hasGeometry ?geom; \
      foaf:name ?name.\
    ?geom geo:asWKT ?wkt.\
    ?pbarea a :PublishArea;\
      geo:asWKT ?fwkt.\
    FILTER(STR(?pbarea) = '" + wkt_query + "')\
    FILTER("+ spatial_relation +"(geof:buffer(?wkt,"+ str(radius) +", uom:metre), ?fwkt))}"

# sparql API
def getSparql(query_string):
  # import requests module
  import requests
  from requests.auth import HTTPBasicAuth

  # making a get request
  headers = {'content-type' : 'application/json'}
  # response = requests.get('https://ogdb.sgis.tw/repositories/disaster?query='+query)
  response = requests.post('https://ogdb.sgis.tw/repositories/disaster', data={"query": query_string}, auth=HTTPBasicAuth(USER, PASSWORD))

  # return request result
  return csvStringToJsonObject(response.text)

def querySpatialRelationsEquals(isInland):
  entity_euqals = []
  
  if ( isInland ):
    if ( "Polygon" in publish_area_type ):
      entity_euqals = getSparql(returnBasicSparqlTESTING(":Building", "geof:sfEquals", publish_area_wkt))
    elif ( "Point" in publish_area_type ):
      entity_euqals = getSparql(returnBasicSparqlTESTING(":Spot", "geof:sfEquals", publish_area_wkt))
    elif ( "Line" in publish_area_type ):
      entity_euqals = getSparql(returnBasicSparqlTESTING(":Road", "geof:sfEquals", publish_area_wkt))
  else:
    if ( "Polygon" in publish_area_type ):
      entity_euqals = getSparql(returnBasicSparqlTESTING(":Coastline :SeaArea", "geof:sfEquals", publish_area_wkt))
  return entity_euqals

def querySpatialEqualsAdmin(query_class, query_values, query_values_class):
  admin_equals = getSparql(returnLimitSparq(query_class, "geof:sfEquals", publish_area_wkt, query_values, query_values_class))

  return admin_equals

def querySpatialRelationsIntersectsAdmin():
  admin_intersects = {}
  
  locate_county = getSparql(returnBasicSparqlTESTING(":County", "geof:sfIntersects", publish_area_wkt))
  county_limit_query = ""
  admin_intersects["county"] = []
  for county in locate_county:
    county_limit_query += "'" + county["name"] + "'"
    admin_intersects["county"].append( county["name"] )
    county_limit_query += " "
  #print(county_limit_query)

  locate_town = getSparql(returnLimitSparq(":Township", "geof:sfIntersects", publish_area_wkt, county_limit_query, ":countyname"))
  town_limit_query = ""
  admin_intersects["township"] = []
  for town in locate_town:
    town_limit_query += "'" + town["name"] + "'"
    admin_intersects["township"].append( town["name"] )
    town_limit_query += " "
  print(town_limit_query)

  locate_vill = getSparql(returnLimitSparq(":Village", "geof:sfIntersects", publish_area_wkt, town_limit_query, ":townshipname"))
  admin_intersects["village"] = []
  for vill in locate_vill:
    admin_intersects["village"].append( vill["name"] )
  
  return admin_intersects

def querySpatialRelationsIntersectsObj(isInland):
  object_intersects = []
  if ( isInland ):
    if ( "Line" in publish_area_type ):
      object_intersects = getSparql(returnSparqlBuffer(":River :Road", "geof:sfIntersects", 1000, publish_area_wkt))
  else:
    if ( "Line" in publish_area_type or "Polygon" in publish_area_type ):
      object_intersects = getSparql(returnSparqlBuffer(":Coastline :SeaArea", "geof:sfIntersects", 50000, publish_area_wkt))
  return object_intersects

def querySpatialRelationsIntersectsHill(county_list):
  admin_hill_intersects = []
  if ( len (county_list) != 0 ):
    for county in county_list:
      result_list = getSparql(returnLimitSparq(":Hill", "geof:sfIntersects", publish_area_wkt, "'"+ str(county) +"'", ":countyname"))
      #print("result_list", result_list)
      for result in result_list:
        admin_hill_intersects.append({"class": result["class"], "name": str(county) + result["name"]})
  
  return admin_hill_intersects

def querySpatialRelationsContains():
  object_contains = []
  
  if ( "Polygon" in publish_area_type ):
    object_contains = getSparql(returnBasicSparqlTESTING(":Building", "geof:sfContains", publish_area_wkt))
  elif ( "Point" in publish_area_type ):
    object_contains = getSparql(returnBasicSparqlTESTING(":Building", "geof:sfIntersects", publish_area_wkt))
    if ( len(object_contains) == 0 ): #在建築物裡的話就不會在路上(?
      object_contains = getSparql(returnBasicSparqlTESTING(":Road", "geof:sfIntersects", publish_area_wkt))

  return object_contains 

def querySpatialRelationsNears(isInland):
  if ( isInland ):
    object_nears = getSparql(returnSparqlDistance(":Spot", 200, publish_area_wkt))
    object_nears += getSparql(returnSparqlDistance(":Place", 200, publish_area_wkt))
    object_nears += getSparql(returnSparqlDistance(":Building", 200, publish_area_wkt))
    object_nears += getSparql(returnSparqlDistance(":Road", 200, publish_area_wkt))

    return object_nears, 200
    if ( len(object_nears) == 0 ):
      object_nears = getSparql(returnSparqlDistance(":Spot :Building", 500, publish_area_wkt))
      return object_nears, 500
    if ( len(object_nears) == 0 ):
      object_nears = getSparql(returnSparqlDistance(":Spot", 3000, publish_area_wkt))
      return object_nears, 3000
    #object_nears += getSparql(returnSparqlDistance(":River", 1000, publish_area_wkt))
    
  else:
    object_nears = getSparql(returnSparqlDistance(":Coastline", 50000, publish_area_wkt))
    return object_nears, 50000
    if ( len(object_nears) == 0 ):
      object_nears = getSparql(returnSparqlDistance(":Coastline", 100000, publish_area_wkt))
      return object_nears, 100000

def querySpatialRelations():
  spatial_analysis_result = {}

  isInland = (len(getSparql(returnBasicSparqlTESTING(":Province", "geof:sfIntersects", publish_area_wkt))) != 0)
  #isInland = False

  ## 2.1 inland
  if (isInland):
    ### 2.1.1 intersects
    print("intersects(admin)...")
    spatial_analysis_result["intersects_admin"] = querySpatialRelationsIntersectsAdmin() 
    print(spatial_analysis_result["intersects_admin"])
    
    ### 2.1.1 equal 相等
    print("equal...")
    admin_equals = []
    if ( len(spatial_analysis_result["intersects_admin"]["village"]) == 1 ):
      querySpatialEqualsAdmin(":Village", spatial_analysis_result["intersects_admin"]["village"][0], "foaf:name")
    elif ( len(spatial_analysis_result["intersects_admin"]["township"]) == 1 ):
      querySpatialEqualsAdmin(":Township", spatial_analysis_result["intersects_admin"]["township"][0], "foaf:name")
    elif ( len(spatial_analysis_result["intersects_admin"]["county"]) == 1 ):
      querySpatialEqualsAdmin(":County", spatial_analysis_result["intersects_admin"]["county"][0], "foaf:name")

    spatial_analysis_result["isEqual"] = admin_equals + querySpatialRelationsEquals(isInland)
    if ( len(spatial_analysis_result["isEqual"]) != 0 ): # end if equal
      print(spatial_analysis_result["isEqual"])
      return spatial_analysis_result

    ### 2.1.3 contain 在之中
    print("contain...")
    #### 2.1.3.1 get admin contains from intersects
    admin_contain = []
    if ( len(spatial_analysis_result["intersects_admin"]["village"]) == 1 ):
      admin_contain.append({'class': 'http://www.semanticweb.org/win/ontologies/2023/1/disaster#Village', 'name': spatial_analysis_result["intersects_admin"]["village"][0]})
      admin_contain.append({'class': 'http://www.semanticweb.org/win/ontologies/2023/1/disaster#Township', 'name': spatial_analysis_result["intersects_admin"]["township"][0]})
      admin_contain.append({'class': 'http://www.semanticweb.org/win/ontologies/2023/1/disaster#County', 'name': spatial_analysis_result["intersects_admin"]["county"][0]})
    elif ( len(spatial_analysis_result["intersects_admin"]["township"]) == 1 ):
      admin_contain.append({'class': 'http://www.semanticweb.org/win/ontologies/2023/1/disaster#Township', 'name': spatial_analysis_result["intersects_admin"]["township"][0]})
      admin_contain.append({'class': 'http://www.semanticweb.org/win/ontologies/2023/1/disaster#County', 'name': spatial_analysis_result["intersects_admin"]["county"][0]})
    elif ( len(spatial_analysis_result["intersects_admin"]["county"]) == 1 ):
      admin_contain.append({'class': 'http://www.semanticweb.org/win/ontologies/2023/1/disaster#County', 'name': spatial_analysis_result["intersects_admin"]["county"][0]})
    
    spatial_analysis_result["isContain"] = admin_contain + querySpatialRelationsContains() # admin + object contain
    print(spatial_analysis_result["isContain"])

    ### 2.1.4 distance
    print("distance...")
    spatial_analysis_result["isNear200"] = []
    object_within = []
    object_near = []
    if ( "臺北市" in spatial_analysis_result["intersects_admin"]["county"] ):
      naer_entity, dist = querySpatialRelationsNears(isInland)
      for entity in naer_entity:
        if ( entity["dist"][:3] == "0.0" ):
          entity.pop('dist', None)
          object_within.append( entity )
        else:
          object_near.append( entity )
      spatial_analysis_result[f"isNear{dist}"] = object_near
      print(dist, spatial_analysis_result[f"isNear{dist}"])
    else:
      print("is not supported yet")

    ### 2.1.5 intersect
    print("intersect(objects)...")
    spatial_analysis_result["isIntersect"] = []
    if ( len(spatial_analysis_result["intersects_admin"]["village"]) > 3 ):
      spatial_analysis_result["isIntersect"] = querySpatialRelationsIntersectsObj(isInland)
    print(spatial_analysis_result["isIntersect"])

    ### 2.1.6 within 包含
    print("within...")
    #### 2.1.6.1 get within from distance
    #for nears_entity in spatial_analysis_result["isNear200"]:
      #if ( nears_entity["dist"][:3] == "0.0" ):
       # nears_entity.pop('dist', None)
        #object_within.append( nears_entity )
    spatial_analysis_result["isWithin"] = object_within + querySpatialRelationsIntersectsHill(spatial_analysis_result["intersects_admin"]["county"])
    print(spatial_analysis_result["isWithin"])

  ## 2.2 on the sea
  else: 
    ### 2.2.1 equal 相等
    print("equal...")
    spatial_analysis_result["isEqual"] = querySpatialRelationsEquals(isInland)
    if ( len(spatial_analysis_result["isEqual"]) != 0 ): # end if equal
      return spatial_analysis_result
    print(spatial_analysis_result["isEqual"])

    ### 2.2.2 intersects
    print("intersects...")
    spatial_analysis_result["isIntersect"] = querySpatialRelationsIntersectsObj(isInland) 
    print(spatial_analysis_result["isIntersect"])

    ### 2.2.3 contain 在之中
    print("contain...")
    #### 2.2.3.1 get admin contains from intersects
    spatial_analysis_result["isContain"] = []
    if ( len(spatial_analysis_result["isIntersect"]) == 1 ):
      spatial_analysis_result["isContain"] = spatial_analysis_result["isIntersect"]
    print(spatial_analysis_result["isContain"])

    ### 2.2.4 distance
    print("distance...")
    near_entity, dist = querySpatialRelationsNears(isInland)
    spatial_analysis_result[f"isNearCoastline{dist}"] = near_entity
    print(spatial_analysis_result[f"isNearCoastline{dist}"])
    
    ### 2.2.6 within 包含
    #### 2.2.6.1 get within from distance
    object_within = []
    for nears_entity in spatial_analysis_result["isNearCoastline50000"]:
      if ( nears_entity["dist"][:3] == "0.0" ):
        nears_entity.pop('dist', None)
        object_within.append( nears_entity )
    spatial_analysis_result["isWithin"] = object_within
  return spatial_analysis_result