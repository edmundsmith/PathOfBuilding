import xml.etree.ElementTree as ET
import hashlib

filetypes = (".lua",".txt")

manifest = ET.parse("manifest.xml")
root = manifest.getroot()

for file in root.iter("File"):
	path = file.get('name')
	if not path.endswith(filetypes):
 		continue
	try:
		old_hash = file.get('sha1')
		hash = hashlib.sha1(open(path, 'rb').read()).hexdigest()
		file.set("sha1", hash)
		if old_hash != hash:
			print("path {} hash changed: now {}".format(path,hash))
	except FileNotFoundError:
		print("file not found, skipping: {}".format(path))


############VERY HACKY#############
#ElementTree re-orders attributes by default sorted() order on Python <=3.7
#This... er... changes that behaviour
import builtins
_sorted = builtins.sorted
builtins.sorted = lambda x,**args:_sorted(x,**args,reverse=True)
	
manifest.write("manifest.xml")

