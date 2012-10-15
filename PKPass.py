import os
import json
import time
import shutil
import zipfile
import functions
import subprocess

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
        self.description = ""

        self.iconLocation = ""
        self.logoLocation = ""
        self.thumbnailLocation = ""
        self.stripLocation = ""
        self.footerLocation = ""
        
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
            "teamIdentifier":     self.teamIdentifier,
            "description":        self.description
        }
        
        # Web Services
        if self.authenticationToken and self.webServiceURL:
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
        
        if self.backgroundColor:
            serialization["backgroundColor"] = self.backgroundColor
        if self.foregroundColor:
            serialization["foregroundColor"] = self.foregroundColor
        if self.labelColor:
            serialization["labelColor"] = self.labelColor
            
        if self.logoText:
            serialization["logoText"] = self.logoText
            
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
        
    def pack(self, outputLocation):
        outputLocation = os.path.abspath(outputLocation)
        if os.path.isdir(outputLocation):
            shutil.rmtree(outputLocation)
        os.makedirs(outputLocation)
        
        passImageLocations = []
        passImageLocations.extend(functions.gather_image_locations(self.iconLocation))
        passImageLocations.extend(functions.gather_image_locations(self.logoLocation))
        passImageLocations.extend(functions.gather_image_locations(self.thumbnailLocation))
        passImageLocations.extend(functions.gather_image_locations(self.stripLocation))
        passImageLocations.extend(functions.gather_image_locations(self.footerLocation))
            
        passInfoFileLocation = '%s/pass.json' % (outputLocation)
        passInfoFile = open(passInfoFileLocation, 'w')
        json.dump(self.serialized(), passInfoFile)
        passInfoFile.close()
        
        for passImageLocation in passImageLocations:
            passImageName = os.path.basename(passImageLocation)
            passImageDestination = '%s/%s' % (outputLocation, passImageName)
            shutil.copyfile(passImageLocation, passImageDestination)
        
    def sign(self, certLocation, certPassword, outputLocation, wwdrCertLocation = 'WWDR.pem'):
        packageLocation = '/tmp/%d.pass' % (int(time.time()))
        self.pack(packageLocation)
        
        certPemLocation = '/tmp/cert.pem'
        subprocess.call([ # Generate Cert
            'openssl', 'pkcs12',
            '-passin', 'pass:%s' % (certPassword),
            '-in', certLocation,
            '-clcerts', '-nokeys',
            '-out', certPemLocation
        ])
        
        keyPemLocation = '/tmp/key.pem'
        subprocess.call([ # Generate Key
            'openssl', 'pkcs12',
            '-passin', 'pass:%s' % (certPassword),
            '-passout', 'pass:%s' % (certPassword),
            '-in', certLocation,
            '-nocerts',
            '-out', keyPemLocation
        ])
        
        manifest = {}
        for fileName in os.listdir(packageLocation):
            hashOutput = functions.check_output([
                'openssl', 'sha1',
                '%s/%s' % (packageLocation, fileName)
            ])

            hashedFileName = hashOutput.split(' ')[-1].strip()
            manifest[fileName] = hashedFileName
            
        manifestFileLocation = '%s/manifest.json' % (packageLocation)
        manifestFile = open(manifestFileLocation, 'w')
        json.dump(manifest, manifestFile)
        manifestFile.close()
        
        subprocess.call([ # Sign Package
            'openssl', 'smime',
            '-passin', 'pass:%s' % (certPassword),
            '-binary', '-sign',
            '-certfile', wwdrCertLocation,
            '-signer', certPemLocation,
            '-inkey', keyPemLocation,
            '-in', '%s/manifest.json' % (packageLocation),
            '-out', '%s/signature' % (packageLocation),
            '-outform', 'DER'
        ])
        
        files = functions.check_output([ # Gather Pass Contents
            'ls', '-r', packageLocation
        ])
        files = [file for file in files.split('\n')[:-1]]
        
        # Zip Package
        os.chdir(packageLocation)
        zipOutputFile = zipfile.ZipFile(outputLocation, 'w')
        for file in files:
            zipOutputFile.write(file)
        
        shutil.rmtree(packageLocation)