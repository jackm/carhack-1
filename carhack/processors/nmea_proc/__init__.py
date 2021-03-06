import logging

import nmea

from carhack.processors import Processor, subscribe

log = logging.getLogger('nmea_proc')


class NMEAProcessor(Processor):
  def __init__(self, pub):
    super(NMEAProcessor, self).__init__(pub)

  @subscribe('gps_nmea.nmea_string')
  def read(self, ts, data):
    obj = None
    try:
      obj = nmea.parse(data)

    except Exception, e:
      print data
      import traceback
      traceback.print_exc()
      return

    if isinstance(obj, nmea.RMC):
      speed = obj.spd_over_grnd * 1.852
      direction = obj.true_course
      latitude = obj.latitude
      longitude = obj.longitude
      if latitude == 0.:
        return
      self.publish('gps.speed_over_ground_rmc', ts, speed)
      self.publish('gps.direction_rmc', ts, direction)
      self.publish('gps.position', ts, (latitude, longitude))

    elif isinstance(obj, nmea.VTG):
      speed = obj.spd_over_grnd_kmph
      direction = obj.true_track
      self.publish('gps.speed_over_ground_vtg', ts, speed)
      self.publish('gps.direction_vtg', ts, direction)

    if isinstance(obj, nmea.GGA):
      altitude = obj.altitude
      latitude = obj.latitude
      longitude = obj.longitude
      if latitude == 0.:
        return
      self.publish('gps.altitude', ts, altitude)
      self.publish('gps.position', ts, (latitude, longitude))


processor = NMEAProcessor
