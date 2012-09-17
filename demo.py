import json
from PKBoardingPass import PKBoardingPass

demoPass = PKBoardingPass("pass.com.example.myExamplePass", "123456", "PKTransitTypeAir")

demoPass.addPrimaryField("origin", "San Francisco", "SFO")
demoPass.addPrimaryField("destination", "London", "LHR")

demoPass.addSecondaryField("board-gate", "F12", "Gate", "Gate changed to %@.")
demoPass.addSecondaryField("board-time", "2012-04-01T0700-8", "Boards", "Boarding time changed to %@.")
demoPass.secondaryFields[-1].setDateStyle()

demoPass.addAuxiliaryField("seat", "7A", "Seat")
demoPass.addAuxiliaryField("passenger-name", "John Appleseed", "Passenger")

demoPass.addBackField("freq-flier-num", "1234-5678", "Frequent flier number")

print json.dumps(demoPass.serialized(), indent = 4)

demoPass.iconLocation = "/Users/me/Desktop/icon.png"
demoPass.sign("/Users/me/Desktop/cert.p12", "passwd", "/Users/me/Desktop/demoPass.pkpass")