from inspect import cleandoc

import folder_paths

import os

# この custom_nodes のスクリプトを import 対象に含める
import sys
this_node_root=os.path.dirname(__file__)
sys.path.append(this_node_root)

import tomllib
import random as rand


class MyRefToml:
    @classmethod
    def INPUT_TYPES(s):
        with open( os.path.join( this_node_root, "src.toml" ), "rb" ) as fileObj:
            obj = tomllib.load( fileObj )
            key_list = [ "<none>", *list( obj.keys() ) ]
        
        return {
            "required":{
                "string": ( "STRING", ),
                "index": ( "INT", {"default":0, "min":0, "max": 1000 } ),
                "random": ("BOOLEAN", {"default":False} ),
                "scale": ( "FLOAT", {"default":1.0, "min":0.1, "max":2.0, "step":0.01 } ),
                "name1": ( key_list, ),
                "name2": ( key_list, ),
                "name3": ( key_list, ),
            },
        }

    CATEGORY = "utils/string"

    RETURN_NAMES = ( "result", "only picked string" )
    RETURN_TYPES = ("STRING","STRING")
    FUNCTION = "execute"

    def execute(self, index, random, scale, string, name1, name2, name3 ):
        with open( os.path.join( this_node_root, "src.toml" ), "rb" ) as fileObj:
            obj = tomllib.load( fileObj )

            picked = ""
            for name in [ name1, name2, name3 ]:
                if name != "<none>":
                    val_list = obj[ name ]
                    val_num = len( val_list )

                    if random:
                        index = rand.randrange( val_num )
                    
                    val = val_list[ index % val_num ]
                    if int(scale * 100) != 100:
                        val = f"({val}:{scale:.2f})"
                        

                        
                    picked = f"{val}, {picked}"

            string = f"{picked}, {string}"
                    
        return (string, picked)

    S_COUNT = 0
    @classmethod
    def IS_CHANGED(s, index, random, scale, string, name1, name2, name3 ):
        global S_COUNT
        S_COUNT += 1
        return S_COUNT


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "MyRefToml": MyRefToml,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "MyRefToml": "MyRefTomlDisp",
}
