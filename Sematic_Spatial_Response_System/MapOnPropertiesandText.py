def MapOnPropertiesandText(hasSpatialDescription):
  hasSpatialDescription_list = list(hasSpatialDescription.keys())
  placename_list = {1:[], 2:[], 3:[], 0: []}
  for spatial_description in hasSpatialDescription_list:
    # print(spatial_description, hasSpatialDescription[spatial_description])
    if ( spatial_description == "hasSpatialDescriptionExact" ):
      if ( len(hasSpatialDescription[spatial_description]) != 0 ):
        for name in hasSpatialDescription[spatial_description]:
          placename = getNameFromOntoClass(name)
          placename_list[1].append(placename)
    elif ( spatial_description == "hasSpatialDescriptionExactCounty" ):
      if ( len(hasSpatialDescription[spatial_description]) != 0 ):
        for name in hasSpatialDescription[spatial_description]:
          placename = f"{getNameFromOntoClass(name)[:-1]}地區"
          placename_list[1].append(placename)
    elif ( spatial_description == "hasSpatialDescriptionRoughBuilding" ):
      if ( len(hasSpatialDescription[spatial_description]) != 0 ):
        for name in hasSpatialDescription[spatial_description]:
          placename = getNameFromOntoClass(name)
          placename_list[3].append(placename)
    elif ( spatial_description == "hasSpatialDescriptionRoughRoad" ):
      if ( len(hasSpatialDescription[spatial_description]) != 0 ):
        for name in hasSpatialDescription[spatial_description]:
          placename = f"在{getNameFromOntoClass(name)}上"
          placename_list[3].append(placename)
    elif ( spatial_description == "hasSpatialDescriptionRoughVillage" ):
      if ( len(hasSpatialDescription[spatial_description]) != 0 ):
        for name in hasSpatialDescription[spatial_description]:
          placename = getNameFromOntoClass(name)
          placename_list[3].append(placename)
    elif ( spatial_description == "hasSpatialDescriptionOnRoad" ):
      if ( len(hasSpatialDescription[spatial_description]) != 0 ):
        for name in hasSpatialDescription[spatial_description]:
          placename = f"在{getNameFromOntoClass(name)}上"
          placename_list[2].append(placename)
    elif ( spatial_description == "hasSpatialDescriptioOnCoastline" ):
      if ( len(hasSpatialDescription[spatial_description]) != 0 ):
        for name in hasSpatialDescription[spatial_description]:
          placename = f"{getNameFromOntoClass(name)[:2]}近海"
          placename_list[1].append(placename)
    elif ( spatial_description == "hasSpatialDescriptioNear200" ):
      if ( len(hasSpatialDescription[spatial_description]) != 0 ):
        for name in hasSpatialDescription[spatial_description]:
          placename = f"鄰近{getNameFromOntoClass(name)}處"
          placename_list[2].append(placename)
    elif ( spatial_description == "hasSpatialDescriptioNear500" ):
      if ( len(hasSpatialDescription[spatial_description]) != 0 ):
        for name in hasSpatialDescription[spatial_description]:
          placename = f"{getNameFromOntoClass(name)}附近"
          placename_list[3].append(placename)
    elif ( spatial_description == "hasSpatialDescriptioNear3000" ):
      if ( len(hasSpatialDescription[spatial_description]) != 0 ):
        for name in hasSpatialDescription[spatial_description]:
          placename = f"{getNameFromOntoClass(name)}周圍"
          placename_list[3].append(placename)
    elif ( spatial_description == "hasSpatialDescriptioNearRoad" ):
      if ( len(hasSpatialDescription[spatial_description]) != 0 ):
        road_list = []
        for road_name in hasSpatialDescription[spatial_description]:
          road_name = getNameFromOntoClass(road_name)
          if ( road_name not in road_list):
            road_list.append(road_name)
        if ( len(road_list) >= 1 ):
          for i in range(0, len(road_list)):
            first_road = road_list[i]
            for j in range(i+1, len(road_list)):
              second_road = road_list[j]
              placename = first_road[:-1] + second_road[:-1] + "路口"
              placename = f"鄰近{placename}處"
              placename_list[2].append(placename)
        else: 
          placename = road_list[0]
          placename = f"鄰近{placename}處"
          placename_list[2].append(placename)
    elif ( spatial_description == "hasSpatialDescriptioNearCoastline50000" ):
      if ( len(hasSpatialDescription[spatial_description]) != 0 ):
        for name in hasSpatialDescription[spatial_description]:
          placename = f"{getNameFromOntoClass(name)[:2]}外海"
          placename_list[2].append(placename)
    elif ( spatial_description == "hasSpatialDescriptioNearCoastline100000" ):
      if ( len(hasSpatialDescription[spatial_description]) != 0 ):
        for name in hasSpatialDescription[spatial_description]:
          placename = f"{getNameFromOntoClass(name)[:2]}外海"
          placename_list[3].append(placename)
    elif ( spatial_description == "hasSpatialDescriptioPlace" ):
      if ( len(hasSpatialDescription[spatial_description]) != 0 ):
        for name in hasSpatialDescription[spatial_description]:
          placename = f"{getNameFromOntoClass(name)}附近"
          placename_list[2].append(placename)
    elif ( spatial_description == "hasSpatialDescriptionRiver" ):
      if ( len(hasSpatialDescription[spatial_description]) != 0 ):
        for name in hasSpatialDescription[spatial_description]:
          placename = getNameFromOntoClass(name)
          placename_list[1].append(placename)
    elif ( spatial_description == "hasSpatialDescriptioSeaArea" ):
      if ( len(hasSpatialDescription[spatial_description]) != 0 ):
        direction_list = ["東", "西", "北", "南"]
        fdirection_list = []
        dircetion_cnt = 0
        placename = ""
        for i in range(0, len(hasSpatialDescription[spatial_description])):
          fdirection_list.append(getNameFromOntoClass(hasSpatialDescription[spatial_description][i]))
        for direction in direction_list:
          if ( direction in fdirection_list):
            dircetion_cnt += 1
            placename += direction
        if ( dircetion_cnt == 1 ):
          placename = f"{placename}部海域"
        elif ( dircetion_cnt == 3 ):
          if ( "西" in placename ):
            placename = "西部海域"
          elif ( "東" in placename):
            placename = "東部海域"
        else:
          placename = f"{placename}海域"
        placename_list[2].append(placename)
    elif ( spatial_description == "hasSpatialDescriptioHill" ):
      if ( len(hasSpatialDescription[spatial_description]) != 0 ):
        county_list = []
        placename = ""
        for name in hasSpatialDescription[spatial_description]:
          name = getNameFromOntoClass(name)[:2]
          if ( name not in county_list ):
            county_list.append(name)
        for county in county_list:
          placename += county
          placename += "和"
        placename = f"{placename[:-1]}山區"
        placename_list[1].append(placename)
    elif ( spatial_description == "hasSpatialDescriptioRoad" ):
      if ( len(hasSpatialDescription[spatial_description]) != 0 ):
        for name in hasSpatialDescription[spatial_description]:
          placename = getNameFromOntoClass(name)
          if ( placename not in placename_list[1] ):
            placename_list[1].append(placename)
    elif ( spatial_description == "hasSpatialDescriptionBasicUnit" ):
      if ( len(hasSpatialDescription[spatial_description]) != 0 ):
        for name in hasSpatialDescription[spatial_description]:
          placename = getNameFromOntoClass(name)
          placename_list[3].append(placename)
    elif ( spatial_description == "hasCounty" ):
      if ( len(hasSpatialDescription[spatial_description]) != 0 ):
        for name in hasSpatialDescription[spatial_description]:
          placename = getNameFromOntoClass(name)
          placename_list[0].append(placename)
    elif ( spatial_description == "hasTownship" ):
      if ( len(hasSpatialDescription[spatial_description]) != 0 ):
        for name in hasSpatialDescription[spatial_description]:
          placename = getNameFromOntoClass(name)
          placename_list[0].append(placename)
    elif ( spatial_description == "hasVillage" ):
      if ( len(hasSpatialDescription[spatial_description]) != 0 ):
        for name in hasSpatialDescription[spatial_description]:
          placename = getNameFromOntoClass(name)
          placename_list[0].append(placename)
  return placename_list