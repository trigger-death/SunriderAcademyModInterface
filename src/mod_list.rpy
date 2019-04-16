init -200 python:
    # Extend from _object so we do not end up in the store or in saved games
    class AcademyModLegacyButton(_object):
        """
        The wrapper class for an the depricated ac_mod_button_list mods.
        """

        def __init__(self,mod):
            """
            @attr mod: The list containing the legacy mod definition parameters.
            """
            self.mod = mod

        @property
        def idle_image(self):
            """
            Get the image used for the button's idle state.
            """
            return self.mod[0]

        @property
        def hover_image(self):
            """
            Get the image used for the button's hover state.
            """
            return self.mod[1]

        def make_action(self):
            """
            Gets the full action for the button which hides main_menu,
            mods_list, and performs the appropriate action.
            """
            if self.mod[2] != False:
                action = Start(self.mod[2])
            elif self.mod[3] != False:
                action = Show(self.mod[3])
            else:
                action = Function(self.mod[4])
            return [Hide("main_menu"),Hide("mods_list"),action]

        def make_button(self):
            """
            Create the image button to display in the mod list.
            """
            return renpy.display.behavior.ImageButton(
                idle_image=self.idle_image,
                hover_image=self.hover_image,
                hover_sound="Sounds/hover1.ogg",
                activate_sound="Sounds/button1.ogg",
                action=self.make_action())

    # Extend from _object so we do not end up in the store or in saved games
    class AcademyModButton(_object):
        """
        The class for an Academy Mod List mod button
        """
        def __init__(self,text=None,idle_image=None,hover_image=None,action=None,condition=None,hide_list=False):
            """
            Required Attributes:

            @attr text: The text to display on the button.
            -or-
            @attr idle_image: The image to use for the button when idle.
            @attr hover_image: The image to use for the button on hover.

            @attr action: The action to perform when pressing the button.

            Optional Attributes:

            @attr condition: The condition to evaluate to see if the button
            should be shown in the mod list.

            @attr hide_list: True if the mods_list screen should be hidden
            after pressing the button. (This can be done in action too, but
            is not recommended if the screen name changes)
            """
            self.text = text
            self.idle_image = idle_image
            self.hover_image = hover_image
            self.action = action
            self.condition = condition
            self.hide_list = hide_list

        def eval_condition(self):
            """
            Evaluates the condition for the mod button, if it has one.
            """
            if self.condition is None:
                return True
            return eval(self.condition)

        def make_action(self):
            """
            Gets the full action for the button with hide_list applied if necessary.
            """
            return [If(self.hide_list,Hide("mods_list")),self.action]

        def make_button(self):
            """
            Create the button to display in the mod list.
            """
            idle = "mods/mod_list/mod_template_base.png"
            hover = "mods/mod_list/mod_template_hover.png"
            if not self.idle_image  is None: idle  = self.idle_image
            if not self.hover_image is None: hover = self.hover_image

            return renpy.display.behavior.ImageButton(
                idle_image=idle,
                hover_image=hover,
                hover_sound="Sounds/hover1.ogg",
                activate_sound="Sounds/button1.ogg",
                action=self.make_action())

        def make_text(self):
            """
            Create the button to display over the button in the mod list.
            """
            if self.text is None:
                # Return empty text if we have None
                return Text("")

            return Text(
                self.text,
                xpos=24,ypos=33,
                yanchor=0.5,
                size=32,
                font="mods/mod_list/TwCenMTStd-Light.otf",
                color="#201F1F")


    # Extend from _object so we do not end up in the store or in saved games
    class AcademyModList(_object):
        """
        Contains all data for the Mod List.
        Mods should be added to the main menu by calling ac_mod.register_main_button().
        """

        def __init__(self):
            """
            @attr version: The version of the installed Mod List

            @attr main_buttons: The list of new AcademyModButton classes that define
            buttons in the main menu mod list.

            @attr label_callbacks: The list for label callbacks, this allows you to
            override the callback without worry of other mods causing conflicts.
            @attr original_label_callback: The callback that is used by the game (if any).
            """
            self.version = '2.0.0.0'

            self.main_buttons = []
            self.label_callbacks = []
            self.original_label_callback = None

        def label_callback(self,label,abnormal):
            """
            The label callback that handles calling of all mod callbacks passed to
            register_label_callback().
            """
            # Call the original label callback FIRST
            if not self.original_label_callback is None:
                self.original_label_callback(label,abnormal)

            # Call each callback in the list, one by one
            for callback in self.label_callbacks:
                callback(label,abnormal)

        def register_label_callback(self,callback):
            """
            Add your label callback to the list DURING AN INIT BLOCK. The later you
            register your callback, the later it will get called in the chain.

            @param callback: Your callback function. This callback must not do anything
            if your mod is disabled.
            """
            self.label_callbacks.append(callback)

        def eval_main_buttons(self):
            """
            Gets a list of all main_menu buttons, for mods that have defined one.

            @returns All buttons where eval_condition() returns True combined with
            the depricated ac_mod_button_list where is_legacy_valid() is True.
            """
            def is_legacy_valid(self, mod):
                """
                Check if a legacy Mod List button has a valid definition and can be
                displayed in the list.

                @param mod: The list containing the legacy mod button definition parameters.
                """
                defined_count = 0
                if mod[2] != False: defined_count += 1
                if mod[3] != False: defined_count += 1
                if mod[4] != False: defined_count += 1
                return defined_count == 1

            return ([mod for mod in self.main_buttons if mod.eval_condition()] +
                    [AcademyModLegacyButton(mod) for mod in ac_mod_button_list if is_legacy_valid(mod)])


        def register_main_button(self,text=None,idle_image=None,hover_image=None,action=None,condition=None,hide_list=False):
            """
            Add a mod and button to the main_menu mods_list screen.

            Required Parameters:

            @param text: The text to display on the mod list button.
            -or-
            @param idle_image: The image to use for the button when idle.
            @param hover_image: The image to use for the button on hover.

            @param action: The action to perform when pressing the mod list button.

            Optional Parameters:

            @param condition: A condition that is passed to eval to check if the
            mod list button is visible.
            @param hide_list: True if the mods_list screen should be hidden when
            clicking the button.

            @returns The constructed AcademyModButton
            """
            mod = AcademyModButton(text=text,idle_image=idle_image,hover_image=hover_image,action=action,condition=condition,hide_list=hide_list)
            self.main_buttons.append(mod)
            return mod

    # The container for the mod list
    ac_mod = AcademyModList()
    # Keep for backwards compatibility, this is referenced in ac_mod.eval_main_buttons().
    ac_mod_button_list = []

init 2 python:
    # Initialize the Mod List label callback override system
    # Sunrider Academy's label callback is setup in an `init 1` block, so we need `init 2` or later.
    ac_mod.original_label_callback = config.label_callback
    config.label_callback = ac_mod.label_callback

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
            text "CHEAT: SKIP COMMON" xpos 150 ypos 407 size 26 color "000" font "mods/mod_list/TwCenMTStd-Light.otf" at tr_menubutton(0.5,150)       
            
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

init 2:
    # Override decision screen and fix optional choice 3 jumping to choice 2 instead.
    # Additionally, decision_extra is now disabled on jump, so that other mods can
    # re-use the decision screen without having to reset decision_extra.
    screen decision:

        modal True
        zorder 100

        imagebutton at tr_decision(0):
            xanchor 0.5
            ypos 0.35
            idle "UI/choice_hover.png"
            hover "UI/choice_base.png"
            hover_sound "Sounds/hover1.ogg"
            activate_sound "Sounds/button1.ogg"
            action (Hide("decision"),SetVariable("decision_extra",False),Jump(choice1_jump))

        imagebutton at tr_decision(0.2):
            xanchor 0.5
            ypos 0.5
            idle "UI/choice_hover.png"
            hover "UI/choice_base.png"
            hover_sound "Sounds/hover1.ogg"
            activate_sound "Sounds/button1.ogg"
            action (Hide("decision"),SetVariable("decision_extra",False),Jump(choice2_jump))

        if decision_extra == True:

            imagebutton at tr_decision(0.4):
                xanchor 0.5
                ypos 0.65
                idle "UI/choice_hover.png"
                hover "UI/choice_base.png"
                hover_sound "Sounds/hover1.ogg"
                activate_sound "Sounds/button1.ogg"
                action (Hide("decision"),SetVariable("decision_extra",False),Jump(choice3_jump)) # Fix choice2_jump being called here

        text choice1_text at tr_decision(0):
            text_align 0.5 xanchor 0.5 ypos 0.39
            size 40
            outlines [ (4, "#282828", 0, 0) ]

        text choice2_text at tr_decision(0.2):
            text_align 0.5 xanchor 0.5 ypos 0.54
            size 40
            outlines [ (4, "#282828", 0, 0) ]

        if decision_extra == True:

            text choice3_text at tr_decision(0.4):
                text_align 0.5 xanchor 0.5 ypos 0.69
                size 40
                outlines [ (4, "#282828", 0, 0) ]

screen mods_list:

    zorder 200
    modal True

    add "mods/mod_list/mods_base.png":
        xalign 0.5 yalign 0.5

    fixed:
        xmaximum 593 ymaximum 801
        xalign 0.5 yalign 0.5

        imagebutton:
            xpos 56 ypos 680
            idle "mods/mod_list/mods_Returnmain_base.png"
            hover "mods/mod_list/mods_Returnmain_hover.png"

            action Hide("mods_list")
            hover_sound "Sounds/hover1.ogg"
            activate_sound "Sounds/button1.ogg"

        frame:
            xsize 460
            xpos 58 ypos 128
            background None

            # Evaluate all buttons once
            $ ac_mod_buttons = ac_mod.eval_main_buttons()

            viewport:
                xsize 538 ysize 514
                if len(ac_mod_buttons) > 7:
                    draggable True
                    mousewheel True
                    scrollbars "vertical"
                child_size (540,max(1,len(ac_mod_buttons)*74-2))

                vbox:
                    spacing 0
                    yfill False
                    for mod in ac_mod_buttons:
                        frame:
                            yfill False
                            ysize 74
                            background None

                            if isinstance(mod, AcademyModButton):
                                imagebutton:
                                    idle "mods/mod_list/mod_template_base.png"
                                    hover "mods/mod_list/mod_template_hover.png"
                                    hover_sound "Sounds/hover1.ogg"
                                    activate_sound "Sounds/button1.ogg"
                                    action mod.make_action()
                                # add renpy.display.behavior.ImageButton(
                                #     "mods/mod_list/mod_template_base.png",
                                #     "mods/mod_list/mod_template_hover.png",
                                #     hover_sound="Sounds/hover1.ogg",
                                #     activate_sound="Sounds/button1.ogg",
                                #     action=[If(mod.hide_main,Hide("main_menu")),If(mod.hide_list,Hide("mods_list")),mod.action]
                                # )
                                #TODO: Support verbose mod names
                                text mod.text:
                                    xpos 24
                                    size 32
                                    font "mods/mod_list/TwCenMTStd-Light.otf"
                                    yanchor 0.5
                                    ypos 33
                                    color "#201F1F"

                            # Legacy Mod List support
                            elif isinstance(mod, AcademyModLegacyButton):
                                imagebutton:
                                    idle mod.idle_image
                                    hover mod.hover_image
                                    hover_sound "Sounds/hover1.ogg"
                                    activate_sound "Sounds/button1.ogg"
                                    action mod.make_action()


            $ del ac_mod_buttons
