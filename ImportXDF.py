#TODO write a description for this script
#@author 
#@category Data
#@keybinding 
#@menupath 
#@toolbar 


#TODO Add User Code Here
import xml.etree.ElementTree as ET

def SanitizeName(myName):
    myOut =""
    for c in myName:
        if c==" ":
            myOut += "_"
        elif c.isalnum():
            myOut += c
    return myOut

filename = (askFile("Select XDF List File", "Go baby go!")).toString()

tree = ET.parse(filename)
root = tree.getroot()

for i in root.iter('XDFFLAG'):
    mask=i.find('mask').text
    title=i.find('title').text
    embeddeddata=i.find('EMBEDDEDDATA')
    mmeaddress=embeddeddata.get('mmedaddress')

    # at least 1 line in XDF was missing mmeaddress
    if mmeaddress == None:
	continue
    address=toAddr(mmeaddress)
    name = SanitizeName("Flag " + mask + " " + title)
    print "createLabel("+mmeaddress+", "+name+", False)"
    removeDataAt(address)
    createLabel(address, name, False)
    
for i in root.iter('XDFCONSTANT'):
    title=i.find('title').text
    embeddeddata=i.find('EMBEDDEDDATA')
    size=embeddeddata.get('mmedelementsizebits')
    
    if size == None:
        continue
    
    mmeaddress=embeddeddata.get('mmedaddress')
    
    if mmeaddress == None:
        continue
    
    address=toAddr(mmeaddress)
    name = SanitizeName("Constant"+size+" " + title)
    print "createLabel("+mmeaddress+", "+name+", False)"
    removeDataAt(address)
    createLabel(address, name, False)

# foreach ($table in $xdf.XDFFORMAT.XDFTABLE)
# {
for i in root.iter('XDFTABLE'):
# 	$columns = $table.XDFAXIS[0].indexcount;
# 	$rows = $table.XDFAXIS[1].indexcount;
# 	$address = $table.XDFAXIS[$table.XDFAXIS.Length - 1].EMBEDDEDDATA.mmedaddress;
    rows=0
    columns=0
    axis = i.findall('XDFAXIS')
    lastaxis = len(axis) - 1
    
    for myaxis in axis:
        if myaxis == axis[lastaxis]:
            data=myaxis.find('EMBEDDEDDATA')
            mmeaddress=data.get('mmedaddress')
        
        indexcount=myaxis.find('indexcount')
        if indexcount == None:
            continue
        count = int(indexcount.text)
        if myaxis.attrib.get('id') == 'x':   
            columns = count
        elif myaxis.attrib.get('id') == 'y':
            rows = count
# 
# 	if ($columns -eq 1)
    if columns == 1:
# 	{
# 		if ($rows -eq 1)
        if rows == 1:
# 		{
# 			$name = "" # this is a checksum 'table' and the name will be clear enough
            name = "" # this is a checksum 'table' and the name will be clear enough
# 		}
# 		else
        else:
# 		{
# 			$name = "CurveTable " + $rows + " Rows"
            name = "CurveTable_" + str(rows) + "_Rows"
# 		}
# 	}
# 	else
    else:
# 	{
# 		if ($rows -eq 1)
        if rows == 1:
# 		{
# 			$name = "CurveTable " + $columns + " Columns"
            name = "CurveTable_" + str(columns) + "_Columns"
# 		}
# 		else
        else:   
# 		{
# 			$name = "SurfaceTable " + $columns + "x" + $rows
			name = "SurfaceTable_" + str(columns) + "x" + str(rows)
# 		}
# 	}
# 
# 	$name = $name + " " + $table.title
    title = i.find('title')
    if title != None:
        name += "_" + title.text
# 
# 
# 	$unused = $builder.AppendLine("MakeNameEx($address, `"$name`", nameFlags);")
    name=SanitizeName(name)
    removeDataAt(address)
    print "createLabel("+mmeaddress+", "+name+", False)"
    address=toAddr(mmeaddress)
    createLabel(address, name, False)
# }
