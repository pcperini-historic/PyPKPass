from PKPass import PKPass

class PKCoupon(PKPass):
    def __init__(self, passTypeIdentifier, serialNumber):
        super(PKCoupon, self).__init__(passTypeIdentifier, serialNumber)
        
        # Style-Specific Information
        self.passType = "coupon"