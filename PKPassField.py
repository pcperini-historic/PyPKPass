textAlignments = [
    "PKTextAlignmentLeft",
    "PKTextAlignmentCenter",
    "PKTextAlignmentRight",
    "PKTextAlignmentJustified",
    "PKTextAlignmentNatural"
]

dateStyles = [
    "PKDateStyleNone",
    "PKDateStyleShort",
    "PKDateStyleMedium",
    "PKDateStyleLong",
    "PKDateStyleFull"
]

timeStyles = [
    "PKTimeStyleNone",
    "PKTimeStyleShort",
    "PKTimeStyleMedium",
    "PKTimeStyleLong",
    "PKTimeStyleFull"
]

numberStyles = [
    "PKNumberStyleDecimal",
    "PKNumberStylePercent",
    "PKNumberStyleScientific",
    "PKNumberStyleSpellOut"
]

class PKPassField:
    def __init__(self, key, value, label = None, changeMessage = None, textAlignment = "PKTextAlignmentNatural"):
        self.key = key
        self.value = value
        self.label = label
        self.changeMessage = changeMessage
        
        # Date Styles
        self.dateStyle = None
        self.timeStyle = None
        self.isRelative = False
        
        # Number Styles
        self.currencyCode = None
        self.numberStyle = None
        
        # Balance
        self.balance = None
        
        if textAlignment in textAlignments:
            self.textAlignment = textAlignment
        else:
            raise ValueError("PKPassField invalid textAlignment %s" % (textAlignment))
            
    def setDateStyle(self, dateStyle = "PKDateStyleFull", timeStyle = "PKTimeStyleFull", isRelative = True):
        if dateStyle in dateStyles:
            self.dateStyle = dateStyle
        else:
            raise ValueError("PKPassField invalid dateStyle %s" % (dateStyle))
            
        if timeStyle in timeStyles:
            self.timeStyle = timeStyle
        else:
            raise ValueError("PKPassField invalid timeStyle %s" % (timeStyle))
            
        self.isRelative = isRelative
        
    def setNumberStyle(self, currencyCode = "USD", numberStyle = "PKNumberStyleDecimal"):
        self.currencyCode = currencyCode
        
        if numberStyle in numberStyles:
            self.numberStyle = numberStyle
        else:
            raise ValueError("PKPassField invalid numberStyle %s" % (numberStyle))
    
    def setBalance(self, balance):
        self.balance = balance
        
    def serialized(self):
        serialization = {
            "key":    self.key,
            "value":  self.value
        }
        
        if self.label:
            serialization["label"] = self.label
        
        if self.changeMessage:
            serialization["changeMessage"] = self.changeMessage
            
        # Date Styles
        if self.dateStyle and self.timeStyle:
            dateStyles = {
                "dateStyle":  self.dateStyle,
                "timeStyle":  self.timeStyle,
                "isRelative": self.isRelative
            }
            
            serialization.update(dateStyles)
            
        # Number Styles
        if self.currencyCode and self.numberStyle:
            numberStyles = {
                "currencyCode": self.currencyCode,
                "numberStyle":  self.numberStyle
            }
            
            serialization.update(numberStyles)
            
        # Balance
        if self.balance:
            serialization["balance"] = self.balance
            
        return serialization