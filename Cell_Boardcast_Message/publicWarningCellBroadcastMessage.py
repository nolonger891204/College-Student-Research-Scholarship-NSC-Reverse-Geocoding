import getPlaceName from getPlaceName

def placeProcess(undefined_place):
  try:
    publish_area_wkt, publish_area_type = geojsonToWKT(undefined_place)
  except:
    print("unknown input!")

def getEventMessage():
  if ( event_code == "earthquake" ):
    message = [f"[地震報告]{occur_time}{occur_place}發生{scale}有感地震，詳細資訊請參考氣象局網站。{institution}"]
    return message
  elif ( event_code == "earthquakeEW" ):
    message = [f"[地震速報]{occur_time}左右{occur_place}發生有感地震，預估震度 4 級以上地區：{effect_place}，慎防強烈搖晃。{institution}"]
    return message
  elif ( event_code == "debrisFlow" ):
    message = [f"[土石流警戒]{occur_place}已發布{scale}土石流警戒，請提高警覺。{institution}"]
    return message
  elif ( event_code == "tsunami" ):
    message = [f"[大雷雨即時訊息]{occur_place}地區即將發生大雷雨，預計持續至{end_time}。請注意強降雨、陣風、雷擊現象，低窪慎防淹水，留意溪水暴漲並注意安全請提高警覺。{institution}"]
    return message
  elif ( event_code == "communicable" ):
    message = [
      f"[疫情警示]{occur_place}已出現登革熱疫情。請做好防蚊措施，主動清除室內外積水容器定期巡查，有發燒、頭痛、關節痛、紅疹等，請儘速就醫接受 NS1 快篩。{institution}",
      f"[疫情警示]{occur_place}已出現傳染性疫情。身體不適請戴口罩立即就醫，並告知旅遊史。{institution}"
    ]
    return message 
  elif ( event_code == "ReservoirDis" ):
    message = [
      f"[水庫放水警戒]{occur_place}因臨時強降雨，將進行排放水。請{effect_place}下游沿岸附近民眾加強注意並遠離河床，以策安全。{institution}",
      f"[水壩放水警戒]{occur_place}因臨時強降雨，將進行排放水。請{effect_place}下游沿岸附近民眾加強注意並遠離河床，以策安全。{institution}"
    ]
    return message 
  elif ( event_code == "airQuality" ):
    message = [
      f"[空品警報]{occur_time}{occur_place}因{reason}，空品已達{scale}，建議留在室內減少戶外活動。{institution}"
    ]
    return message 
  elif ( event_code == "roadClose" ):
    message = [
      f"[公路封閉警戒]{occur_place}{reason}，今{occur_time}禁止進入，{process_time}時全面封閉。已進入者勿逗留，儘速撤離。{institution}",
      f"[公路封閉警戒]{occur_place}{reason}，建議勿進入。已進入者勿逗留，儘速撤離。{institution}"
    ]
    return message 
  elif ( event_code == "HurricFrcWnd" ):
    message = [
      f"[颱風強風告警]{occur_place}，附近即將出現12級平均風或14級陣風以上風力。請停止戶外活動並立即掩蔽。{institution}"
    ]
    return message 
  elif ( event_code == "electric" ):
    message = [
      f"[電力中斷通知]{occur_place}{occur_place}，{reason}，供電能力不足。{process_time}開始執行緊急分區輪流停電。{institution}"
    ]
    return message 

def publicWarningCellBroadcastMessage(input):
  global event_code
  event_code = input["event_code"]
  global occur_time 
  occur_time = input["occur_time"]
  global reason 
  reason = input["reason"]
  global process_time 
  process_time = input["process_time"]
  global scale
  scale = input["scale"]
  global end_time
  end_time = input["end_time"]
  global institution
  institution = input["institution"]
  global undefined_occur_place
  undefined_occur_place = input["occur_place"]
  global undefined_effect_place
  undefined_effect_place = input["effect_place"]
  global occur_place
  global effect_place

  occur_place_dict = {}
  effect_place_dict = {}

  if ( undefined_occur_place != None ):
    occur_place_dict = placeProcess(undefined_occur_place)
  if ( undefined_effect_place != None ):
    effect_place_dict = placeProcess(undefined_effect_place)

  if ( undefined_occur_place != None and undefined_effect_place == None ):
    effect_place = ""
    for i in range(1,4):
      if ( occur_place_dict[i] != [] ):
        for occur_placename in occur_place_dict[i]:
          occur_place = occur_placename
          return(getEventMessage())
  elif ( undefined_occur_place == None and undefined_effect_place != None ):
    occur_place = ""
    for i in range(1,4):
      if ( effect_place_dict[i] != [] ):
        for effect_placename in effect_place_dict[i]:
          effect_place = effect_placename
          return(getEventMessage())
  elif ( undefined_occur_place != None and undefined_effect_place != None ):
    for i in range(1,4):
      if ( occur_place_dict[i] != [] ):
        for occur_placename in occur_place_dict[i]:
          occur_place = occur_placename
          for j in range(1,4):
            if ( len(effect_place_dict[j]) != 0 ):
              for effect_placename in effect_place_dict[i]:
                effect_place = effect_placename
                return(getEventMessage())
  else:
    return(getEventMessage())