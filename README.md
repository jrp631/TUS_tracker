# Documentation for TUS Tracker

[TUS public API](https://datos.santander.es/api/rest/datasets/control_flotas_posiciones.json)

TUS provides a public API that allows users to access real-time data about bus lines, including their positions and routes. This API is useful for tracking buses in Santander, Spain. Altough the provided documentation is scarce and outdated. 

**Sample JSON response**:

```json
{"summary":{"items":40336,"items_per_page":50,"pages":807,"current_page":1},"resources":[
    {
      "wgs84_pos:long":"-3.8131307728304242",
      "ayto:instante":"2025-07-30T06:01:08.563Z",
      "gn:coordY":"4813062",
      "gn:coordX":"434332",
      "ayto:linea":"51",
      "ayto:velocidad":"16",
      "dc:modified":"2025-07-30T09:50:58.009Z",
      "ayto:vehiculo":"77",
      "wgs84_pos:lat":"43.4657099670395",
      "ayto:estado":"5",
      "uri":"http://datos.santander.es/api/datos/control_flotas_posiciones/2586.json"},
    {
      "wgs84_pos:long":"-3.8107067736201556",
      "ayto:instante":"2025-07-30T06:01:33.567Z",
      "gn:coordY":"4813052",
      "gn:coordX":"434528",
      "ayto:linea":"51",
      "ayto:velocidad":"27",
      "dc:modified":"2025-07-30T09:50:58.009Z",
      "ayto:vehiculo":"77",
      "wgs84_pos:lat":"43.465637122210495",
      "ayto:estado":"5",
      "uri":"http://datos.santander.es/api/datos/control_flotas_posiciones/2587.json"},
    {
      "wgs84_pos:long":"-3.8080201987373314",
      "ayto:instante":"2025-07-30T06:01:58.560Z",
      "gn:coordY":"4813017",
      "gn:coordX":"434745",
      "ayto:linea":"51",
      "ayto:velocidad":"31",
      "dc:modified":"2025-07-30T09:50:58.009Z",
      "ayto:vehiculo":"77",
      "wgs84_pos:lat":"43.46534097281779",
      "ayto:estado":"5",
      "uri":"http://datos.santander.es/api/datos/control_flotas_posiciones/2588.json"} 
      ...]
}
```

**Lineas disponibles**: 1,2,3,4,5C1,5C2,6C1,6C2,7C1,7C2,11,12,13,14,15,16,17,18,24C1,24C2,99,E1,N1,N2,N3

diccionario con las lineas {lineas, posiciones[NUMERO_AUTOBUSES_DE_LINEA]}
