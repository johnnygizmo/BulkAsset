import bpy
import os

def item_callback(self,context):
        directory = context.space_data.params.directory
        d = str(directory).split('\'')
        directory = d[1]
        cat = open(os.path.join(str(directory),"blender_assets.cats.txt"))
        cats = cat.readlines()
        cat.close()
        
        output = [("","Catalog","",0),("00000000-0000-0000-0000-000000000000","Unassigned","",0)]
        i=1
        for line in cats:
            if line[0:1] == "#":
                continue
            if line.strip() == "":
                continue
            if line[0:7] == "VERSION":
                continue
            data = line.split(":")
            output.append((data[0],data[1],"",i))
            i += 1
        return output