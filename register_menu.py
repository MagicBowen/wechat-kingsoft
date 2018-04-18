import os
import sys
sys.path.append("lib/itchat")
import itchatmp
 
menu = {
    "button":[
    {    
        "type":"click",
        "name":"秋叶青",
        "key":"kingsoft-qiuye"
    },
    {    
        "type":"click",
        "name":"李复",
        "key":"kingsoft-lifu"
    }
    ]
}
    
def register_menu():
    r = itchatmp.menu.create(menu)
    print('register menu complete!')