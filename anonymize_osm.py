# Author:  Philippe Latylippe
# Repo:    https://github.com/philippelatulippe/osm-file-anonymizer
# Licence: Simplified BSD (2-clause), see ./LICENSE

from xml.dom import minidom
import sys

id_map = {}

minlat=float("+inf")
maxlat=float("-inf")
minlon=float("+inf")
maxlon=float("-inf")

dom = minidom.parse(sys.stdin)

document = dom.documentElement

def lat2str(lat):
    return "{:.7f}".format(lat)
def lon2str(lon):
    return "{:.7f}".format(lon)

def process_element(node):
    for attr in node.attributes.items():
        #print(attr,end=" ")
        name = attr[0]
        value = attr[1]
        # remove tags with action="delete"
        if name == "action" and value == "delete":
            node.parent.removeChild(node)
        # remove attribute action="modify"
        elif name == "action" and value == "modify":
            node.removeAttribute(name)
        # remove attrib uid, user, changeset, timestamp
        elif (name == "uid" or name == "user" or name == "changeset" or
              name == "changeset" or name == "timestamp"):
            node.removeAttribute(name)
        # We need to keep the version attribute on the root tag
        if node.localName != "osm" and name == "version":
            node.setAttribute(name, "1")
        # create new IDs and update references.
        elif name == "id" or name == "ref":
            if value in id_map:
                replacement_id = id_map[value]
            else:
                replacement_id = str(len(id_map) + 1)
                id_map[value] = replacement_id

            node.setAttribute(name,replacement_id)
        # move map area to (0,0)
        elif name == "lat":
            node.setAttribute(name, lat2str(float(value)-minlat))
        elif name == "lon":
            node.setAttribute(name, lon2str(float(value)-minlon))
            
    #print()

def traverse(node):
    if node.attributes:
        process_element(node)

    for child in node.childNodes:
        traverse(child)


#Get the bounds of the map, so that we can move it to (0,0)
bounds_tags = document.getElementsByTagName("bounds")

for bound in bounds_tags:
    minlat = min(minlat, float(bound.attributes["minlat"].value))
    maxlat = max(maxlat, float(bound.attributes["maxlat"].value))
    minlon = min(minlon, float(bound.attributes["minlon"].value))
    maxlon = max(maxlon, float(bound.attributes["maxlon"].value))

#Now that we know the miximum bounds, we need to move them
for bound in bounds_tags:
    bound.setAttribute("minlat",lat2str(float(bound.attributes["minlat"].value)-minlat))
    bound.setAttribute("maxlat",lat2str(float(bound.attributes["maxlat"].value)-minlat))
    bound.setAttribute("minlon",lon2str(float(bound.attributes["minlon"].value)-minlon))
    bound.setAttribute("maxlon",lon2str(float(bound.attributes["maxlon"].value)-minlon))

traverse(document)




print(document.toprettyxml(newl=""))
