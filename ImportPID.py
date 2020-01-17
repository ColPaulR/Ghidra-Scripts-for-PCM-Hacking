#Imports a file with lines in the form "symbolName 0xADDRESS"
#@category Data
#@author 

f = askFile("Select PID List File", "Go baby go!")

pid = {}
for line in file(f.absolutePath):  # note, cannot use open(), since that is in GhidraScript
    parts = line.split(" ",1)
    pid[int(parts[0],base=16)]=parts[1]

baseAddress=currentProgram.getAddressFactory().getAddress("0x1f70")
myListing=currentProgram.listing

for index in range (0,308):
	parameterId = myListing.getDataAt(baseAddress).getValue().getValue()<<8
	parameterId += myListing.getDataAt(baseAddress.add(1)).getValue().getValue()

	functionAddress = myListing.getDataAt(baseAddress.add(5)).getValue().getValue()<<16
	functionAddress += myListing.getDataAt(baseAddress.add(6)).getValue().getValue()<<8
	functionAddress += myListing.getDataAt(baseAddress.add(7)).getValue().getValue()
	
	functionAddress &= 0xffffff
	functionName = "GetPid_"+hex(parameterId)

	if parameterId in pid:
		functionName += "_" + pid[parameterId]
	
	createLabel(currentProgram.getAddressFactory().getAddress("0x{:06x}".format(functionAddress)), functionName, False)

	baseAddress = baseAddress.add(8)



