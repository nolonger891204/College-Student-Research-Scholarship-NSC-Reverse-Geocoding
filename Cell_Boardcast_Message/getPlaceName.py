import querySpatialRelations from querySpatialRelations
import RulesReasoning from RulesReasoning
import MapOnPropertiesandText from MapOnPropertiesandText
import geojsonToWKT, csvStringToJsonObject, getClassandFromIri, getNameFromOntoClass from base

def getPlaceName(publish_area):
    global publish_area_type
    global publish_area_wkt
    publish_area_wkt, publish_area_type = geojsonToWKT(publish_area)
    spatial_analysis_result = querySpatialRelations()
    hasSpatialDescription = RulesReasoning(spatial_analysis_result)
    result = MapOnPropertiesandText(hasSpatialDescription)
    return result

