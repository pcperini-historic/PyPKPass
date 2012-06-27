from PKPass import PKPass

transitTypes = [
    "PKTransitTypeAir",
    "PKTransitTypeTrain",
    "PKTransitTypeBus",
    "PKTransitTypeBoat",
    "PKTransitTypeGeneric"
]

class PKBoardingPass(PKPass):
    def __init__(self, passTypeIdentifier, serialNumber, transitType = "PKTransitTypeGeneric"):
        super(PKBoardingPass, self).__init__(passTypeIdentifier, serialNumber)
        
        # Style-Specific Information
        self.passType = "boardingPass"
        
        if transitType in transitTypes:
            self.transitType = transitType
        else:
            raise ValueError("PKBoardingPass invalid transitType: %s" % (transitType))
            
    def serialized(self):
        serialization = super(PKBoardingPass, self).serialized()
        
        # Style-Specific Information
        serialization[self.passType]["transitType"] = self.transitType
        
        return serialization