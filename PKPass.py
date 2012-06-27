from PKPassLocation import PKPassLocation
from PKPassBarcode import PKPassBarcode
from PKPassField import PKPassField

class PKPass(object):
    def __init__(self, passTypeIdentifier, serialNumber):
        # Standard
        self.passTypeIdentifier = passTypeIdentifier
        self.serialNumber = serialNumber
        
        self.formatVersion = 1
        self.organizationName = ""
        self.teamIdentifier = ""
        
        # Web Service
        self.authenticationToken = None
        self.webServiceURL = None
        
        # Relevance
        self.locations = []
        self.relevantDate = None
        
        # Visual Appearance
        self.barcode = None
        self.backgroundColor = None
        self.foregroundColor = None
        self.labelColor = None
        self.logoText = None
        
        # Style-Specific Information
        self.passType = "generic"
        
        self.headerFields = []
        self.primaryFields = []
        self.secondaryFields = []
        self.auxiliaryFields = []
        self.backFields = []
        
    def addRelevantLocation(self, latitude, longitude, altitude = 0, relevantText = None):
        location = PKPassLocation(latitude, longitude, altitude, relevantText)
        self.locations.append(location)
        
    def setBarcode(self, message, format = "PKBarcodeFormatQR", messageEncoding = "iso-8859-1", altText = None):
        barcode = PKPassBarcode(message, format, messageEncoding, altText)
        self.barcode = barcode
        
    def addField(self, destination, key, value, label, changeMessage, textAlignment):
        field = PKPassField(key, value, label, changeMessage, textAlignment)
        destination.append(field)
        
    def addHeaderField(self, key, value, label = None, changeMessage = None, textAlignment = "PKTextAlignmentNatural"):
        self.addField(self.headerFields, key, value, label, changeMessage, textAlignment)
        
    def addPrimaryField(self, key, value, label = None, changeMessage = None, textAlignment = "PKTextAlignmentNatural"):
        self.addField(self.primaryFields, key, value, label, changeMessage, textAlignment)
        
    def addSecondaryField(self, key, value, label = None, changeMessage = None, textAlignment = "PKTextAlignmentNatural"):
        self.addField(self.secondaryFields, key, value, label, changeMessage, textAlignment)
        
    def addAuxiliaryField(self, key, value, label = None, changeMessage = None, textAlignment = "PKTextAlignmentNatural"):
        self.addField(self.auxiliaryFields, key, value, label, changeMessage, textAlignment)
        
    def addBackField(self, key, value, label = None, changeMessage = None, textAlignment = "PKTextAlignmentNatural"):
        self.addField(self.backFields, key, value, label, changeMessage, textAlignment)
        
    def serialized(self):
        
        # Standard
        serialization = {
            "passTypeIdentifier": self.passTypeIdentifier,
            "formatVersion":      self.formatVersion,
            "organizationName":   self.organizationName,
            "serialNumber":       self.serialNumber,
            "teamIdentifier":     self.teamIdentifier
        }
        
        # Web Services
        if self.authenticationToken and webServiceURL:
            webService = {
                "authenticationToken":  self.authenticationToken,
                "webServiceURL":        self.webServiceURL
            }
            
            serialization.update(webService)
            
        # Relevance
        if self.locations:
            serialization["locations"] = [location.serialized() for location in self.locations]
        if self.relevantDate:
            serialization["relevantDate"] = self.relevantDate
            
        # Visual Appearance
        if self.barcode:
            serialization["barcode"] = self.barcode.serialized()
            
        visualAppearance = {}
            
        if self.headerFields:
            visualAppearance["headerFields"] = [field.serialized() for field in self.headerFields]
        if self.primaryFields:
            visualAppearance["primaryFields"] = [field.serialized() for field in self.primaryFields]
        if self.secondaryFields:
            visualAppearance["secondaryFields"] = [field.serialized() for field in self.secondaryFields]
        if self.auxiliaryFields:
            visualAppearance["auxiliaryFields"] = [field.serialized() for field in self.auxiliaryFields]
        if self.backFields:
            visualAppearance["backFields"] = [field.serialized() for field in self.backFields]
            
        serialization[self.passType] = visualAppearance
        
        return serialization