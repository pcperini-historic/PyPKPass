class PKPassLocation:
    def __init__(self, latitude, longitude, altitude = 0, relevantText = None):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.relevantText = relevantText
        
    def serialized(self):
        serialization = {
            "latitude":    self.latitude,
            "longitude":   self.longitude,
        }
        
        if self.altitude:
            serialization["altitude"] = self.altitude
            
        if self.relevantText:
            serialization["relevantText"] = self.relevantText
            
        return serialization