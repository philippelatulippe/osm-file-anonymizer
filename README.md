Anonymize OSM XML files
=======================

Intent: submit bug reports with exported data from JOSM without revealing too
much about where you go.

The script works with standard input and output. It has no parameters.

This script only removes information that cannot be removed from within
JOSM. Any OSM tag containing identifying information must be removed
manually. The best way to do that is to use "select all" in JOSM and look at
the list of tags, then use the search tool to see which nodes and ways have
this tag.

What this script does:

* adjust all nodes so that the top left corner of the bounding area as it (0,0)
* remove action tags (When you delete things in JOSM, they do not get deleted 
  from the .osm file, they simply get marked with *action="delete"*)
* remove the XML attributes: uid, user, changeset, timestamp
* set the node versions to "1"
* rewrite the IDs starting from "1", and update the references

**There's absolutely no guarantee a dedicated person won't be able to match
your file to nodes in OpenStreetMap.**

