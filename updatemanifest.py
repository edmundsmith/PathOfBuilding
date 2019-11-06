import xml.etree.ElementTree as ET
import hashlib

filetypes = (".lua",".txt")

manifest = ET.parse("manifest.xml")
root = manifest.getroot()

for file in root.iter("File"):
	path = file.get('name')
	if not path.endswith(filetypes):
		print("Skipping file type {}".format(path[-4:]))
		continue
	try:
		hash = hashlib.sha1(open(path, 'rb').read()).hexdigest()
		file.set("sha1", hash)
		print("path {} hash {}".format(path,hash))
	except FileNotFoundError:
		print("file not found, skipping: {}".format(path))
		continue



############VERY HACKY#############
#ElementTree re-orders attributes by default sorted() order on Python <=3.7
#This... er... changes that behaviour
import builtins
_sorted = builtins.sorted
builtins.sorted = lambda x,**args:_sorted(x,**args,reverse=True)
	
manifest.write("manifest.xml")

