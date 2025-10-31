init python:
    import time

testsuite global:
    setup:
        $ _test.timeout = 4.0
        $ _test.transition_timeout = 0.05

    before testsuite:
        if not screen "main_menu":
            run MainMenu(confirm=False)

    teardown:
        exit


testsuite default:
    description "Default project testsuite"

    before testcase:
        ## Go to the test screen, even if we've crashed in a prior test
        if not screen "tutorials":
            if not screen "main_menu":
                run MainMenu(confirm=False)

            if screen "main_menu":
                run Start()
                advance until screen "tutorials"

    teardown:
        click "That's enough for now." until not screen "tutorials"
        advance until screen "main_menu"
        # click "Quit"


    testsuite blank:
        testcase do_nothing:
            pass

    testsuite blank2:
        testcase do_nothing2:
            pass


    ## Run the testcases
    testcase player_experience:
        $ preferences.text_cps = 0

        scroll "Bar" until "Player Experience"
        click "Player Experience" until not screen "tutorials"
        advance until screen "choice"
        click "Yes."

        # Dialogue after menu.
        advance
        advance
        advance

        # Rollback to the menu.
        click button 4
        click button 4
        click button 4
        click button 4

        # Roll forward.
        click button 5
        click button 5

        # Back again to the menu.
        click button 4
        click button 4

        # Roll forward.
        keysym "K_PAGEDOWN"
        keysym "K_PAGEDOWN"

        # Back again.
        keysym "K_PAGEUP"
        keysym "K_PAGEUP"

        click "No."
        advance until screen "tutorials"

    testcase new_game:
        scroll "Bar" until "Creating a New Game"
        click "Creating a New Game" until not screen "tutorials"
        advance until screen "tutorials"

    testcase dialogue:
        scroll "Bar" until "Writing Dialogue"
        click "Writing Dialogue" until not screen "tutorials"
        advance until screen "tutorials"

    testcase images:
        scroll "Bar" until "Adding Images"
        click "Adding Images" until not screen "tutorials"
        advance until screen "tutorials"

    testcase transitions:
        scroll "Bar" until "Transitions"
        click "Transitions" until not screen "tutorials"
        advance until screen "tutorials"

    testcase music:
        scroll "Bar" until "Music and Sound Effects"
        click "Music and Sound Effects" until not screen "tutorials"
        advance until screen "tutorials"

    testcase choices:
        scroll "Bar" until "Choices and Python"
        click "Choices and Python" until not screen "tutorials"
        advance until screen "choice"
        click "Yes, I do."
        advance until screen "choice"
        click "Yes."
        advance until screen "tutorials"

    testcase input:
        scroll "Bar" until "Input and Interpolation"
        click "Input and Interpolation" until not screen "tutorials"
        advance until screen "input"
        type "Tom"
        keysym "K_BACKSPACE"
        type "m"
        keysym "K_LEFT"
        keysym "K_RIGHT"
        keysym "K_RETURN"
        advance until screen "tutorials"

    testcase positioning_images:
        scroll "Bar" until "Positioning Images"
        click "Positioning Images" until not screen "tutorials"
        advance until screen "tutorials"

    testcase video:
        scroll "Bar" until "Video Playback"
        click "Video Playback" until not screen "tutorials"
        advance until screen "tutorials"


    testcase nvl_mode:
        scroll "Bar" until "NVL Mode"
        click "NVL Mode" until not screen "tutorials"
        advance until eval ("nvl_menu" in renpy.game.context().modes) # screen "nvl_choice"
        click "Yes."
        advance until screen "tutorials"

    testcase tools:
        scroll "Bar" until "Tools and the Interactive Director"
        click "Tools and the Interactive Director" until not screen "tutorials"
        advance until screen "tutorials"

        # Not actually testing the various tools yet.

    testcase building:
        scroll "Bar" until "Building Distributions"
        click "Building Distributions" until not screen "tutorials"
        advance until screen "tutorials"

    testcase text_tags:
        scroll "Bar" until "Text Tags, Escapes, and Interpolation"
        click "Text Tags, Escapes, and Interpolation" until not screen "tutorials"
        advance until screen "tutorials"

    testcase character_objects:
        scroll "Bar" until "Character Objects"
        click "Character Objects" until not screen "tutorials"
        advance until screen "tutorials"

    testcase simple_displayables:
        scroll "Bar" until "Simple Displayables"
        click "Simple Displayables" until not screen "tutorials"
        advance until screen "tutorials"

    testcase transition_gallery:
        $ _test.transition_timeout = 60.0

        scroll "Bar" until "Transition Gallery"
        click "Transition Gallery" until not screen "tutorials"
        advance until screen "choice"
        click "Simple" until not screen "choice"
        advance until screen "choice"
        click "ImageDissolve" until not screen "choice"
        advance until screen "choice"
        click "MoveTransition" until not screen "choice"
        advance until screen "choice"
        click "CropMove" until not screen "choice"
        advance until screen "choice"
        click "PushMove" until not screen "choice"
        advance until screen "choice"
        click "AlphaDissolve" until not screen "choice"
        advance until screen "choice"
        click "something else" until not screen "choice"
        advance until screen "tutorials"

    testcase position_properties:
        scroll "Bar" until "Position Properties"
        click "Position Properties" until not screen "tutorials"
        advance until screen "choice"
        click "xpos .75 ypos .25"
        advance until screen "tutorials"

    testcase transforms:
        scroll "Bar" until "Transforms and Animation"
        click "Transforms and Animation" until not screen "tutorials"
        advance until screen "tutorials"

    testcase transform_properties:
        scroll "Bar" until "Transform Properties"
        click "Transform Properties" until not screen "tutorials"
        advance until screen "tutorials"

    testcase gui_customization:
        scroll "Bar" until "GUI Customization"
        click "GUI Customization" until not screen "tutorials"
        advance until screen "tutorials"

    testcase styles:
        scroll "Bar" until "Styles and Style Properties"
        click "Styles and Style Properties" until not screen "tutorials"
        advance until screen "choice"
        click "Style basics." until not screen "choice"
        advance until screen "choice"
        click "General style properties." until not screen "choice"
        advance until screen "choice"
        click "Text style properties." until not screen "choice"
        advance until screen "choice"
        click "Window and Button style properties." until not screen "choice"
        advance until screen "choice"
        click "Bar style properties." until not screen "choice"
        advance until screen "choice"
        click "Box, Grid, and Fixed style properties." until not screen "choice"
        advance until screen "choice"
        click "The Displayable Inspector." until not screen "choice"
        advance until screen "choice"
        click "That's all I want to know." until not screen "choice"
        advance until screen "tutorials"

    testcase screens:
        scroll "Bar" until "Screen Basics"
        click "Screen Basics" until not screen "tutorials"
        advance until screen "choice"

        click "What screens can do." until not screen "choice"
        advance until screen "choice"
        click "Yes." until not screen "choice"
        advance until screen "choice"

        click "How to show screens." until not screen "choice"
        advance until "Since we can't display dialogue at the same time"
        advance until screen "simple_screen"
        click "Okay" until not screen "simple_screen"
        advance until screen "choice"

        click "Passing parameters to screens." until not screen "choice"
        advance until screen "parameter_screen"
        ## We need to insist on closing the screen. May have to do with transitions
        click "Okay" until not screen "parameter_screen"
        advance until "The call screen statement can also take arguments"
        advance until screen "parameter_screen"
        click "Okay" until not screen "parameter_screen"
        advance until screen "choice"

        click "Screen properties." until not screen "choice"
        advance until screen "modal_example"
        ## We need to insist on closing the screen. May have to do with transitions
        click "Close This Screen" until not screen "modal_example"
        advance until screen "choice"

        click "Special screen statements." until not screen "choice"
        advance until screen "choice"

        click "Using other screens." until not screen "choice"
        advance until screen "choice"

        click "That's it." until not screen "choice"


    testcase screen_displayables:
        scroll "Bar" until "Screen Displayables"
        click "Screen Displayables" until not screen "tutorials"
        advance until screen "choice"
        click "Common properties" until not screen "choice"
        advance until screen "choice"
        click "Adding images" until not screen "choice"
        advance until screen "choice"
        click "Text" until not screen "choice"
        advance until screen "choice"
        click "Buttons" until not screen "choice"
        advance until screen "choice"
        click "Bars" until not screen "choice"
        advance until screen "choice"
        click "Viewports" until not screen "choice"
        advance until screen "choice"
        click "Imagemaps" until not screen "choice"
        advance until screen "imagemap_example"
        click "Science" until not screen "imagemap_example"
        advance until screen "choice"
        click "That's all" until not screen "choice"

        advance until screen "tutorials"

    testcase translations:
        scroll "Bar" until "Translations"
        click "Translations" until not screen "tutorials"
        advance until screen "tutorials"


    testcase out_of_game:
        click "Back"
        click "Back"

        click "Skip"

        click "Back"

        $ _preferences.self_voicing = False
        $ _preferences.afm_time = 1

        click "Auto"
        scroll "Bar" until "Player Experience"
        click "Player Experience" until not screen "tutorials"
        click "Auto"
        click "History"

        pause .5

        click "Save"
        pause .5

        click "Save Slot 1"
        pause 0.2
        if "Yes":
            click "Yes"

        click "Load"
        pause .5

        click "Load Slot 1"
        click "Yes"

        click "Prefs"
        pause .5

        click "About"
        pause .5

        click "Help"
        pause .5

        click "Main Menu"
        click "Yes"

        click "Load"
        pause .5

        click "Load Slot 1"

        advance until screen "choice"
        click "Yes."
        advance until screen "tutorials"
