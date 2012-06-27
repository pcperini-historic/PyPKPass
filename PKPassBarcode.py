formats = [
    "PKBarcodeFormatQR",
    "PKBarcodeFormatPDF417",
    "PKBarcodeFormatAztec",
    "PKBarcodeFormatText"
]

class PKPassBarcode:
    def __init__(self, message, format = "PKBarcodeFormatQR", messageEncoding = "iso-8859-1", altText = None):
        self.message = message
        self.messageEncoding = messageEncoding
        self.altText = altText
        
        if format in formats:
            self.format = format
        else:
            raise ValueError("PKPassBarcode invalid format %s" % (format))
            
    def serialized(self):
        serialization = {
            "message":         self.message,
            "format":          self.format,
            "messageEncoding": self.messageEncoding,
        }
        
        if self.altText:
            serialization["altText"] = self.altText
            
        return serialization