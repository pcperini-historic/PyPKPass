import os
import json
import time
import shutil
import subprocess

from PKPassLocation import PKPassLocation
from PKPassBarcode import PKPassBarcode
from PKPassField import PKPassField


# provides compatibility with python < 2.7
def check_output(*popenargs, **kwargs):
    r"""Run command with arguments and return its output as a byte string.

    If the exit code was non-zero it raises a CalledProcessError.  The
    CalledProcessError object will have the return code in the returncode
    attribute and output in the output attribute.

    The arguments are the same as for the Popen constructor.  Example:

    >>> check_output(["ls", "-l", "/dev/null"])
    'crw-rw-rw- 1 root root 1, 3 Oct 18  2007 /dev/null\n'

    The stdout argument is not allowed as it is used internally.
    To capture standard error in the result, use stderr=STDOUT.

    >>> check_output(["/bin/sh", "-c",
    ...               "ls -l non_existent_file ; exit 0"],
    ...              stderr=STDOUT)
    'ls: non_existent_file: No such file or directory\n'
    """
    if 'stdout' in kwargs:
        raise ValueError('stdout argument not allowed, it will be overridden.')
    process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
    output, unused_err = process.communicate()
    retcode = process.poll()
    if retcode:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]
        raise subprocess.CalledProcessError(retcode, cmd)
    return output


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
        if self.iconLocation:
            rootIconLocation = os.path.splitext(self.iconLocation)[0]
            rootIconExtension = os.path.splitext(self.iconLocation)[1]
            retinaIconLocation = '%s@2x%s' % (rootIconLocation, rootIconExtension)
            
            if os.path.exists(self.iconLocation):
                passImageLocations.append(self.iconLocation)
            if os.path.exists(retinaIconLocation):
                passImageLocations.append(retinaIconLocation)
            
        if self.logoLocation:
            rootLogoLocation = os.path.splitext(self.logoLocation)[0]
            rootLogoExtension = os.path.splitext(self.logoLocation)[1]
            retinaLogoLocation = '%s@2x%s' % (rootLogoLocation, rootLogoExtension)
            
            if os.path.exists(self.logoLocation):
                passImageLocations.append(self.logoLocation)
            if os.path.exists(retinaLogoLocation):
                passImageLocations.append(retinaLogoLocation)
            
        passInfoFileLocation = '%s/pass.json' % (outputLocation)
        passInfoFile = open(passInfoFileLocation, 'w')
        json.dump(self.serialized(), passInfoFile)
        passInfoFile.close()
        
        for passImageLocation in passImageLocations:
            passImageName = os.path.basename(passImageLocation)
            passImageDestination = '%s/%s' % (outputLocation, passImageName)
            shutil.copyfile(passImageLocation, passImageDestination)
        
    def sign(self, certLocation, certPassword, outputLocation):
        packageLocation = '/tmp/%d.pass' % (int(time.time()))
        self.pack(packageLocation)
        
        subprocess.call([ # Generate Cert
            'openssl', 'pkcs12',
            '-passin', 'pass:%s' % (certPassword),
            '-in', certLocation,
            '-clcerts', '-nokeys',
            '-out', '/tmp/cert.pem'
        ])
        
        subprocess.call([ # Generate Key
            'openssl', 'pkcs12',
            '-passin', 'pass:%s' % (certPassword),
            '-in', certLocation,
            '-nocerts',
            '-out', '/tmp/key.pem'
        ])
        
        manifest = {}
        for fileName in os.listdir(packageLocation):
            # python 2.7 or greater
            if hasattr(subprocess, 'check_output'):
                hashOutput = subprocess.check_output([
                    'openssl', 'sha1',
                    '%s/%s' % (packageLocation, fileName)
                ])
            else:
                hashOutput = check_output([
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
            '-signer', '/tmp/cert.pem',
            '-inkey', '/tmp/key.pem',
            '-in', '%s/manifest.json' % (packageLocation),
            '-out', '%s/signature' % (packageLocation),
            'xs-outform', 'DER'
        ])

        outputLocation = os.path.abspath(outputLocation)
        os.chdir(packageLocation)
        subprocess.call([  # Zip Pass
            'zip', outputLocation, '*'
        ])
        
        shutil.rmtree(packageLocation)