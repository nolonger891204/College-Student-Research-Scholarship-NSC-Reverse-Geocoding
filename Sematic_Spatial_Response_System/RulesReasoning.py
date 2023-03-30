def RulesReasoning(spatial_analysis_result):
  ## 3.1 read owl
  import owlready2 as owl
  onto = owl.get_ontology("./OSD.owl").load()
  isEqual = onto.isEqual
  isContain = onto.isContain
  isNear200 = onto.isNear200
  isNear500 = onto.isNear500
  isNear3000 = onto.isNear3000
  isNearCoastline50000 = onto.isNearCoastline50000
  isNearCoastline100000 = onto.isNearCoastline100000
  isIntersect = onto.isIntersect
  isWithin = onto.isWithin

  if ( "Polygon" in publish_area_type ):
    query_area = onto.Polygon(publish_area_wkt)
  elif ( "Point" in publish_area_type ):
    query_area = onto.Point(publish_area_wkt)
  elif ( "Line" in publish_area_type ):
    query_area = onto.Line(publish_area_wkt)
  
  spatial_relations = list(spatial_analysis_result.keys())
  for item in spatial_relations:
    if ( item != "intersects_admin" ):
      for entity in spatial_analysis_result[item]:
        onto_class = getClassandFromIri(entity["class"])
        entity_name = entity["name"]
        entity = onto[onto_class](entity_name, namespace = onto)
        if ( item == "isEqual" ):
          query_area.isEqual.append(entity)
        elif ( item == "isContain" ):
          query_area.isContain.append(entity)
        elif ( item == "isNear200" ):
          query_area.isNear200.append(entity)
        elif ( item == "isNear500" ):
          query_area.isNear500.append(entity)
        elif ( item == "isNear3000" ):
          query_area.isNear3000.append(entity)
        elif ( item == "isNearCoastline50000" ):
          query_area.isNearCoastline50000.append(entity)
        elif ( item == "isNearCoastline100000" ):
          query_area.isNearCoastline100000.append(entity)
        elif ( item == "isIntersect" ):
          query_area.isIntersect.append(entity)
        elif ( item == "isWithin" ):
          query_area.isWithin.append(entity)
    else:
      for county in spatial_analysis_result["intersects_admin"]["county"]:
        entity = onto["County"](county, namespace = onto)
      for town in spatial_analysis_result["intersects_admin"]["township"]:
        entity = onto["Township"](town, namespace = onto)
      for vill in spatial_analysis_result["intersects_admin"]["village"]:
        entity = onto["Village"](vill, namespace = onto)
  
  return SWRLQeury(onto, query_area)

# 4. SWRL query 
def SWRLQeury(onto, query_area):
  import owlready2 as owl
  with onto:
    class hasSpatialDescriptionExact(onto.PublishArea >> onto.Feature):
      pass
    class hasSpatialDescriptionExactCounty(onto.PublishArea >> onto.Feature):
      pass
    class hasSpatialDescriptionRoughBuilding(onto.PublishArea >> onto.Feature):
      pass
    class hasSpatialDescriptionRoughRoad(onto.PublishArea >> onto.Feature):
      pass
    class hasSpatialDescriptionRoughVillage(onto.PublishArea >> onto.Feature):
      pass
    class hasSpatialDescriptionOnRoad(onto.PublishArea >> onto.Feature):
      pass
    class hasSpatialDescriptioOnCoastline(onto.PublishArea >> onto.Feature):
      pass
    class hasSpatialDescriptioNear200(onto.PublishArea >> onto.Feature):
      pass
    class hasSpatialDescriptioNear500(onto.PublishArea >> onto.Feature):
      pass
    class hasSpatialDescriptioNear3000(onto.PublishArea >> onto.Feature):
      pass
    class hasSpatialDescriptioNearRoad(onto.PublishArea >> onto.Feature):
      pass
    class hasSpatialDescriptioNearCoastline50000(onto.PublishArea >> onto.Feature):
      pass
    class hasSpatialDescriptioNearCoastline100000(onto.PublishArea >> onto.Feature):
      pass
    class hasSpatialDescriptioPlace(onto.PublishArea >> onto.Feature):
      pass
    class hasSpatialDescriptionRiver(onto.PublishArea >> onto.Feature):
      pass
    class hasSpatialDescriptioSeaArea(onto.PublishArea >> onto.Feature):
      pass
    class hasSpatialDescriptioHill(onto.PublishArea >> onto.Feature):
      pass
    class hasSpatialDescriptioRoad(onto.PublishArea >> onto.Feature):
      pass
    class hasSpatialDescriptionBasicUnit(onto.PublishArea >> onto.Feature):
      pass
    class hasCounty(onto.PublishArea >> onto.County):
      pass
    class hasTownship(onto.PublishArea >> onto.Township):
      pass
    class hasVillage(onto.PublishArea >> onto.Village):
      pass

    ## 4.1 hasSpatialDescriptionExact
    rule_exact_entity = owl.Imp()
    rule_exact_entity.set_as_rule("PublishArea(?area), Feature(?name), isEqual(?area, ?name) -> hasSpatialDescriptionExact(?area, ?name)")
    
    rule_exact_county = owl.Imp()
    rule_exact_county.set_as_rule("County(?area), Feature(?name), isEqual(?area, ?name) -> hasSpatialDescriptionExactCounty(?area, ?name)")


    ## 4.2 hasSpatialDescriptionRough
    ### ex: 花蓮縣、某建物、...
    rule_rough_building = owl.Imp()
    rule_rough_building.set_as_rule("Polygon(?area), Building(?name), isWithin(?area, ?name) -> hasSpatialDescriptionRoughBuilding(?area, ?name)")

    rule_rough_road = owl.Imp()
    rule_rough_road.set_as_rule("Polygon(?area), Road(?name), isWithin(?area, ?name) -> hasSpatialDescriptionRoughRoad(?area, ?name)")

    ## 4.3 hasSpatialDescriptionInside
    ### ex: 開山里、某建物、...
    rule_inside1 = owl.Imp()
    rule_inside1.set_as_rule("Point(?area), Village(?name), isContain(?area, ?name) -> hasSpatialDescriptionRoughVillage(?area, ?name)")

    rule_inside2 = owl.Imp()
    rule_inside2.set_as_rule("Point(?area), Building(?name), isContain(?area, ?name) -> hasSpatialDescriptionRoughBuilding(?area, ?name)")

    ## 4.4 hasSpatialDescriptionOn
    ### 以大見小(道路版) ex: 羅斯福路上
    rule_on_road = owl.Imp()
    rule_on_road.set_as_rule("Point(?area), Road(?name), isWithin(?area, ?name) -> hasSpatialDescriptionOnRoad(?area, ?name)")

    rule_on_coastline = owl.Imp()
    rule_on_coastline.set_as_rule("PublishArea(?area), Coastline(?name), isWithin(?area, ?name) -> hasSpatialDescriptioOnCoastline(?area, ?name)")

    ## 4.5 hasSpatialDescriptioNearOO
    ### ex: 鄰近羅斯福路、101附近
    rule_near_200 = owl.Imp()
    rule_near_200.set_as_rule("PublishArea(?area), Spot(?name), isNear200(?area, ?name) -> hasSpatialDescriptioNear200(?area, ?name)")

    rule_near_500 = owl.Imp()
    rule_near_500.set_as_rule("PublishArea(?area), Spot(?name), isNear500(?area, ?name) -> hasSpatialDescriptioNear500(?area, ?name)")
    
    rule_near_3000 = owl.Imp()
    rule_near_3000.set_as_rule("PublishArea(?area), Spot(?name), isNear3000(?area, ?name) -> hasSpatialDescriptioNear3000(?area, ?name)")

    rule_near_road = owl.Imp()
    rule_near_road.set_as_rule("PublishArea(?area), Road(?name), isNear200(?area, ?name) -> hasSpatialDescriptioNearRoad(?area, ?name)")

    rule_near_coastline_50000 = owl.Imp()
    rule_near_coastline_50000.set_as_rule("PublishArea(?area), Coastline(?name), isNearCoastline50000(?area, ?name) -> hasSpatialDescriptioNearCoastline50000(?area, ?name)")

    rule_near_coastline_100000 = owl.Imp() 
    rule_near_coastline_100000.set_as_rule("PublishArea(?area), Coastline(?name), isNearCoastline100000(?area, ?name) -> hasSpatialDescriptioNearCoastline100000(?area, ?name)")
    
    ## 4.6 hasSpatialDescriptioPlace
    ### ex: 公館
    rule_place = owl.Imp()
    rule_place.set_as_rule("Polygon(?area), Place(?name), isWithin(?area, ?name) -> hasSpatialDescriptioPlace(?area, ?name)")

    ## 4.7 hasSpatialDescriptionRiver
    ### ex: 濁水溪
    rule_river = owl.Imp()
    rule_river.set_as_rule("Line(?area), River(?name), isIntersect(?area, ?name) -> hasSpatialDescriptionRiver(?area, ?name)")

    ## 4.8 hasSpatialDescriptioSeaArea
    rule_seaarea = owl.Imp()
    rule_seaarea.set_as_rule("PublishArea(?area), SeaArea(?name), isIntersect(?area, ?name) -> hasSpatialDescriptioSeaArea(?area, ?name)")

    ## 4.9 hasSpatialDescriptioHill
    rule_seaarea = owl.Imp()
    rule_seaarea.set_as_rule("Polygon(?area), Hill(?name), isWithin(?area, ?name) -> hasSpatialDescriptioHill(?area, ?name)")

    ## 4.10 hasSpatialDescriptioRoad
    rule_road_intersect = owl.Imp()
    rule_road_intersect.set_as_rule("Line(?area), Road(?name), isIntersect(?area, ?name) -> hasSpatialDescriptioRoad(?area, ?name)")

    rule_road_within = owl.Imp()
    rule_road_within.set_as_rule("Line(?area), Road(?name), isWithin(?area, ?name) -> hasSpatialDescriptioRoad(?area, ?name)")

    ## 4.X hasSpatialDescriptionBasicUnit
    ### ex: 開山里
    rule_contain = owl.Imp()
    rule_contain.set_as_rule("Polygon(?area), Village(?name), isContain(?area, ?name) -> hasSpatialDescriptionBasicUnit(?area, ?name)")

    ## 4.X+1 hasCounty/hasTownship/hasVillage
    ### ex: 台北市(作為補述)
    rule_county = owl.Imp()
    rule_county.set_as_rule("PublishArea(?area), County(?name) -> hasCounty(?area, ?name)")

    rule_township = owl.Imp()
    rule_township.set_as_rule("PublishArea(?area), Township(?name) -> hasTownship(?area, ?name)")
    
    rule_village = owl.Imp()
    rule_village.set_as_rule("PublishArea(?area), Village(?name) -> hasVillage(?area, ?name)")

  owl.sync_reasoner_pellet(infer_property_values = True, infer_data_property_values = True)

  hasSpatialDescription = {
      "hasSpatialDescriptionExact": query_area.hasSpatialDescriptionExact, 
      "hasSpatialDescriptionExactCounty": query_area.hasSpatialDescriptionExactCounty, 
      "hasSpatialDescriptionRoughBuilding": query_area.hasSpatialDescriptionRoughBuilding, 
      "hasSpatialDescriptionRoughRoad": query_area.hasSpatialDescriptionRoughRoad,
      "hasSpatialDescriptionRoughVillage": query_area.hasSpatialDescriptionRoughVillage,
      "hasSpatialDescriptionOnRoad": query_area.hasSpatialDescriptionOnRoad,
      "hasSpatialDescriptioOnCoastline": query_area.hasSpatialDescriptioOnCoastline,
      "hasSpatialDescriptioNear200": query_area.hasSpatialDescriptioNear200,
      "hasSpatialDescriptioNear500": query_area.hasSpatialDescriptioNear500,
      "hasSpatialDescriptioNear3000": query_area.hasSpatialDescriptioNear3000,
      "hasSpatialDescriptioNearRoad": query_area.hasSpatialDescriptioNearRoad,
      "hasSpatialDescriptioNearCoastline50000": query_area.hasSpatialDescriptioNearCoastline50000,
      "hasSpatialDescriptioNearCoastline100000": query_area.hasSpatialDescriptioNearCoastline100000,
      "hasSpatialDescriptioPlace": query_area.hasSpatialDescriptioPlace,
      "hasSpatialDescriptionRiver": query_area.hasSpatialDescriptionRiver,
      "hasSpatialDescriptioSeaArea": query_area.hasSpatialDescriptioSeaArea,
      "hasSpatialDescriptioHill": query_area.hasSpatialDescriptioHill,
      "hasSpatialDescriptioRoad": query_area.hasSpatialDescriptioRoad,
      "hasSpatialDescriptionBasicUnit": query_area.hasSpatialDescriptionBasicUnit,
      "hasCounty": query_area.hasCounty,
      "hasTownship": query_area.hasTownship,
      "hasVillage": query_area.hasVillage
  }

  return hasSpatialDescription