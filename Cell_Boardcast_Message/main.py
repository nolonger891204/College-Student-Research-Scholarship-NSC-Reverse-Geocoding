# pip install owlready2

import publicWarningCellBroadcastMessage from publicWarningCellBroadcastMessage

publicWarningCellInput = {
    "event_code": "", # "earthquake", "debrisFlow", "earthquakeEW", "tsunami", "communicable", "ReservoirDis", "airQuality", "roadClose", "HurricFrcWnd", "evacuation", "electric"
    "occur_time": "",
    "occur_place": "", # geojson
    "reason": "",
    "process_time": "",
    "scale": "",
    "end_time": "",
    "effect_place": "", # geojson
    "institution": ""
}

publicWarningCellBroadcastMessage(publicWarningCellInput)