PyPKPass
========

A series of Python objects for the construction, management, and serialization of iOS PassKit passes.

### Coming Soon ###
Builtin support for transporting PKPasses.
Pre-rolled Flask-based support for PassKit webServices.

### A Certified Mess ###
Like all Apple endeavors, the amount of signature hoops one must jump through to create a `.pkpass` is immense. However, PyPKPass attempts to reduce the amount of strife on you by requiring only 1 file for certification.

> The private key of your pass type, in `.p12` format. This can be gotten by opening Keychain Access.app, finding your Pass Type ID certificate (which you made [here](https://developer.apple.com/ios/manage/passtypeids/index.action), right?), and exporting the _PRIVATE KEY_ as a `.p12` file.

You'll need this files for signing passes. Optionally, you can provide your own WWDR certificate. If you have any problems, Google around (there's plenty of tutorials out there) or feel free to email me.

### PKPass ###
- `passTypeIdentifier`: Pass type identifier, as issued by Apple. The value must correspond with your signing certificate.
- `serialNumber`: Serial number that uniquely identifies the pass. No two passes with the same pass type identifier may have the same serial number.
- `organizationName`: Display name of the organization that originated and signed the pass.
- `teamIdentifier`: Team identifier of the organization that originated and signed the pass, as issued by Apple.

- `iconLocation`: The Unix path of the pass' icon. Standard @2x scaling name schemes apply.
- `logoLocation`: The Unix path of the pass' logo. Standard @2x scaling name schemes apply.
- `thumbnailLocation`: The Unix path of the pass' thumbnail. Standard @2x scaling name schemes apply.
- `stripLocation`: The Unix path of the pass' strip image. Standard @2x scaling name schemes apply.
- `footerLocation`: The Unix path of the pass' footer. Standard @2x scaling name schemes apply.

- `authenticationToken`: The authentication token to use with the web service.
- `webServiceURL`: The URL of a web service that conforms to the API described in [Pass Kit Web Service Reference](https://developer.apple.com/library/prerelease/ios/documentation/PassKit/Reference/PassKit_WebService/WebService.html#//apple_ref/doc/uid/TP40011988). The web service must use the HTTPS protocol and includes the leading https://.

- `locations`: Locations where the pass is relevant. For example, the location of your store.
- `relevantDate`: Date and time when the pass becomes relevant. For example, the start time of a movie.

- `barcode`: A PKPassBarcode object.
- `backgroundColor`: Background color of the pass, specified as an CSS-style RGB triple. For example, rgb(23, 187, 82).
- `foregroundColor`: Foreground color of the pass, specified as a CSS-style RGB triple. For example, rgb(100, 10, 110).
- `labelColor`: Color of the label text, specified as a CSS-style RGB triple. For example, rgb(255, 255, 255). If omitted, the label color is determined automatically.
- `logoText`: Text displayed next to the logo on the pass.

- `passType`: The key which identifies the type of pass. This is automatically set by PKPass and its subclasses.

- `headerFields`: Fields to be displayed prominently on the front of the pass.
- `primaryFields`: Fields to be displayed prominently on the front of the pass.
- `secondaryFields`: Fields to be displayed on the front of the pass.
- `auxiliaryFields`: Additional fields to be displayed on the front of the pass.
- `backFields`: Fields to be on the back of the pass.

**__init__**

    __init__(self, passTypeIdentifier, serialNumber)

> Initializes a new PKPass object with the given `passTypeIdentifier` and `serialNumber`.

**addRelevantLocation**

    addRelevantLocation(self, latitude, longitude, altitude = 0, relevantText = None)

> Creates a new PKPassLocation and adds it to this PKPass's `locations` list.

- `latitude`: Latitude, in degrees, of the location.
- `longitude`: Longitude, in degrees, of the location.
- `altitude`: Altitude, in meters, of the location. Ignored if 0.
- `relevantText`: Text displayed on the lock screen when the pass is currently relevant. For example, a description of the nearby location such as “Store nearby on 1st and Main.”

**setBarcode**

    setBarcode(self, message, format = "PKBarcodeFormatQR", messageEncoding = "iso-8859-1", altText = None)
    
> Creates a new PKPassBarcode and sets it to this PKPass's `barcode` variable.

- `message`: Message or payload to be displayed as a barcode.
- `format`: Barcode format.
- `messageEncoding`: Text encoding that is used to convert the message from the string representation to a data representation to render the barcode. The value is typically iso-8859-1, but you may use another encoding that is supported by your barcode scanner and software.
- `altText`: Text displayed near the barcode. For example, a human-readable version of the barcode data in case the barcode doesn’t scan.

**addField**

    addField(self, destination, key, value, label, changeMessage, textAlignment)
    
> Creates a new PKPassField and adds it to `destination`.

- `destination`: The list to which the new PKPassField should be added
- `key`: The key must be unique within the scope of the entire pass. For example, “departure-gate”.
- `value`: Value of the field. For example, 42.
- `label`: Label text for the field.
- `changeMessage`: Format string for the alert text that is displayed when the pass is updated. The format string may contain the escape %@, which is replaced with the field’s new value. For example, “Gate changed to %@.” If you don’t specify a change message, the user isn’t notified when the field changes.
- `textAlignment`: Alignment for the field’s contents.

**addHeaderField**

    addHeaderField(self, key, value, label = None, changeMessage = None, textAlignment = "PKTextAlignmentNatural")

> Calls `addField` with this PKPass's `headerFields` variable as `destination`.

**addPrimaryField**

    addPrimaryField(self, key, value, label = None, changeMessage = None, textAlignment = "PKTextAlignmentNatural")

> Calls `addField` with this PKPass's `primaryFields` variable as `destination`.


**addSecondaryField**

    addSecondaryField(self, key, value, label = None, changeMessage = None, textAlignment = "PKTextAlignmentNatural")
    
> Calls `addField` with this PKPass's `secondaryFields` variable as `destination`.

**addAuxiliaryField**

    addAuxiliaryField(self, key, value, label = None, changeMessage = None, textAlignment = "PKTextAlignmentNatural")
    
> Calls `addField` with this PKPass's `auxiliaryFields` variable as `destination`.

**addBackField**

    addBackField(self, key, value, label = None, changeMessage = None, textAlignment = "PKTextAlignmentNatural")
    
> Calls `addField` with this PKPass's `backFields` variable as `destination`.

**serialized**

    serialized(self)
    
> Returns a JSON-valid `dict` object representing this PKPass. `None` values will not be serialized.

**pack**

    pack(self, outputLocation)
    
> Creates a package-style directory containing this pass, serialized into `pass.json`, its icon files, and its logo files.

**sign**

    sign(self, certLocation, certPassword, outputLocation, wwdrCertLocation = 'WWDR.pem')
    
> Creates a signed, compressed `.pkpass` file containing this pass' package.

--

### PKBoardingPass (PKPass) ###
- `transitType`: Type of transit.

--

### PKCoupon (PKPass) ###

--

### PKEventTicket (PKPass) ###
 
--

### PKStoreCard (PKPass) ###

--

### PKPassBarcode ###
- `message`: Message or payload to be displayed as a barcode.
- `format`: Barcode format.
- `messageEncoding`: Text encoding that is used to convert the message from the string representation to a data representation to render the barcode. The value is typically iso-8859-1, but you may use another encoding that is supported by your barcode scanner and software.
- `altText`: Text displayed near the barcode. For example, a human-readable version of the barcode data in case the barcode doesn’t scan.

**__init__**

    __init__(self, message, format = "PKBarcodeFormatQR", messageEncoding = "iso-8859-1", altText = None)

> Initializes a new PKPassBarcode object with the given `message`, `format`, `messageEncoding`, and `altText`.

**serialized**

    serialized(self)

> Returns a JSON-valid `dict` object representing this PKPassBarcode. `None` values will not be serialized.

--

### PKPassField ###
- `key`: The key must be unique within the scope of the entire pass. For example, “departure-gate”.
- `value`: Value of the field. For example, 42.
- `label`: Label text for the field.
- `changeMessage`: Format string for the alert text that is displayed when the pass is updated. The format string may contain the escape %@, which is replaced with the field’s new value. For example, “Gate changed to %@.” If you don’t specify a change message, the user isn’t notified when the field changes.
- `textAlignment`: Alignment for the field’s contents.

**__init__**

    __init__(self, key, value, label = None, changeMessage = None, textAlignment = "PKTextAlignmentNatural")
    
> Initializes a new PKPassField object with the given `key`, `value`, `label`, `changeMessage`, and `textAlignment`.

**setDateStyle**

    setDateStyle(self, dateStyle = "PKDateStyleFull", timeStyle = "PKTimeStyleFull", isRelative = True)
   
> Adds date styling information to this PKPassField.
    
- `dateStyle`: Style of date to display.
- `timeStyle`: Style of time to display.
- `isRelative`: If true, the label’s value is displayed as a relative date; otherwise, it is displayed as an absolute date.

**setNumberStyle**

    setNumberStyle(self, currencyCode = "USD", numberStyle = "PKNumberStyleDecimal")

> Adds number styling information to this PKPassField.

- `currencyCode`: ISO 4217 currency code for the field’s value.
- `numberStyle`: Style of number to display.

**setBalance**

    setBalance(self, balance)

> Sets the balance of this PKPassField. Only appropriate for use with `PKStoreCard`s.

- `balance`: Current balance of the store card.

--

### PKPassLocation ###
- `latitude`: Latitude, in degrees, of the location.
- `longitude`: Longitude, in degrees, of the location.
- `altitude`: Altitude, in meters, of the location. Ignored if 0.
- `relevantText`: Text displayed on the lock screen when the pass is currently relevant. For example, a description of the nearby location such as “Store nearby on 1st and Main.”

**__init__**

    __init__(self, latitude, longitude, altitude = 0, relevantText = None)

> Initializes a new PKPassLocation object with the given `latitude`, `longitude`, `altitude`, and `relevantText`.

**serialized**

    serialized(self)
    
> Returns a JSON-valid `dict` object representing this PKPassLocation. `None` values will not be serialized.