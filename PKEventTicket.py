from PKPass import PKPass

class PKEventTicket(PKPass):
    def __init__(passTypeIdentifier, serialNumber):
        super(PKEventTicket, self).__init__(passTypeIdentifier, serialNumber)
        
        # Style-Specific Information
        self.passType = "eventTicket"