from GenNcCode import *

modelName = 'ironman_2'
stlModel = StlModel()
stlModel.readStlFile('./model/%s.stl' % modelName)
printParams = PrintParams(stlModel)
nccode = genNcCode(printParams)
print(nccode)
f = open("./gcode/%s_GCode.gcode" % modelName, "w+")
f.write(nccode)
