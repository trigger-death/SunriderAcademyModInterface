init -99 python:
    ac_mod_button_list=[]

init 1:
    screen main_menu:

        add "mainmenu_background" at tr_holobutton(0)

        add "UI/main_logo.png" xpos 50 ypos 20 at tr_menubutton(0.5,50)
        add "UI/main_versionbar.png" xpos 0 ypos 1037 at tr_menubutton(0,0)
        add "UI/main_buttonbar.png" xpos 105 ypos 384 at tr_menubutton(0.5,105)
        
        text "[config.name] V[config.version]" font "Fonts/SourceCodePro-Regular.ttf" xpos 10 ypos 1053 size 15

        if CENSOR == False:

            text 'DENPA EDITION' font "Fonts/SourceCodePro-Regular.ttf" xpos 10 ypos 1038 size 15

        if CENSOR == True:

            text 'STEAM EDITION' font "Fonts/SourceCodePro-Regular.ttf" xpos 10 ypos 1038 size 15

        add "UI/main_ava.png" at tr_menubutton(0.5,0)
        add "UI/main_sola.png" at tr_menubutton(0.7,0)
        add "UI/main_chigara.png" at tr_menubutton(0.9,0)
        add "UI/main_asaga.png" at tr_menubutton(1.1,0)
                
        imagebutton at tr_menubutton(0.5,130):
            xpos 130 ypos 445
            idle "UI/main_start_base.png"
            hover "UI/main_start_hover.png"
            hover_sound "Sounds/hover1.ogg"
            activate_sound "Sounds/button1.ogg"
            action (Hide("main_menu"),Start())
            
        if renpy.seen_label("m9_asagaend") == True or renpy.seen_label("m0_ava_graduationend") == True or renpy.seen_label("m0_chigaraend") == True or renpy.seen_label("m10_solagraduation") == True or cheat == True:
            imagebutton at tr_menubutton(0.5,132):
                xpos 133 ypos 390
                idle "UI/campusmap_button_base.png"
                hover "UI/campusmap_button_hover.png"
                
                activate_sound "Sounds/button1.ogg"
                action (Hide("main_menu"),SetVariable("skipcommon",True),Start())
            text "CHEAT: SKIP COMMON" xpos 145 ypos 405 color "000" at tr_menubutton(0.5,145)        
            
        imagebutton at tr_menubutton(0.7,130):
            xpos 130 ypos 540
            idle "UI/main_load_base.png"
            hover "UI/main_load_hover.png"
            hover_sound "Sounds/hover1.ogg"
            activate_sound "Sounds/button1.ogg"
            action Show("load")
            
        imagebutton at tr_menubutton(0.9,130):
            xpos 130 ypos 635
            idle "UI/main_preferences_base.png"
            hover "UI/main_preferences_hover.png"
            hover_sound "Sounds/hover1.ogg"
            activate_sound "Sounds/button1.ogg"
            action Show("preferences")
            
        imagebutton at tr_menubutton(1.1,130):
            xpos 130 ypos 730
            idle "UI/main_bonus_base.png"
            hover "UI/main_bonus_hover.png"
            hover_sound "Sounds/hover1.ogg"
            activate_sound "Sounds/button1.ogg"
            action Show("gallery_back")

        imagebutton at tr_menubutton(1.3,130):
            xpos 130 ypos 825
            idle "mods/Mod_list/main_mods_base.png"
            hover "mods/Mod_list/main_mods_hover.png"
            hover_sound "Sounds/hover1.ogg"
            activate_sound "Sounds/button1.ogg"
            action Show("mods_list")
            
        imagebutton at tr_menubutton(1.5,130):
            xpos 130 ypos 920
            idle "UI/main_quit_base.png"
            hover "UI/main_quit_hover.png"
            hover_sound "Sounds/hover1.ogg"
            activate_sound "Sounds/button1.ogg"
            action Quit()

screen mods_list:

    zorder 200
    modal True

    add "mods/mod_list/mods_base.png":
        xalign 0.5 yalign 0.5

    imagebutton:
        xpos 720 ypos 820
        idle "mods/mod_list/mods_Returnmain_base.png"
        hover "mods/mod_list/mods_Returnmain_hover.png"

        action Hide("mods_list")
        hover_sound "Sounds/hover1.ogg"
        activate_sound "Sounds/button1.ogg"

    $i = 0
    
    for x in ac_mod_button_list:
        $ yposbuttonmenu = 270 + i*74
        if x[2] != False and x[3] == False and x[4] == False:
            imagebutton:
                xpos 720 ypos yposbuttonmenu 
                idle x[0]
                hover x[1]
                hover_sound "Sounds/hover1.ogg"
                activate_sound "Sounds/button1.ogg"
                action Hide("main_menu"),Hide("mods_list"),Start(x[2])
        if x[3] != False and x[2] == False and x[4] == False:
            imagebutton:
                xpos 720 ypos yposbuttonmenu 
                idle x[0]
                hover x[1]
                hover_sound "Sounds/hover1.ogg"
                activate_sound "Sounds/button1.ogg"
                action Hide("main_menu"),Hide("mods_list"),Show(x[3])
        if x[4] != False and x[3] == False and x[2] == False:
            imagebutton:
                xpos 720 ypos yposbuttonmenu 
                idle x[0]
                hover x[1]
                hover_sound "Sounds/hover1.ogg"
                activate_sound "Sounds/button1.ogg"
                action Hide("main_menu"),Hide("mods_list"),Function(x[4])
        $i += 1 
