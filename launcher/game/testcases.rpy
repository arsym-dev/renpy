testsuite global:
    teardown:
        exit

testcase change_language:
    parameter lang = [
        "arabic", "danish", "finnish", "french", "german",
        "greek", "indonesian", "italian", "japanese", "korean",
        "malay", "persian", "piglatin", "polish", "portuguese",
        "russian", "schinese", "spanish", "tchinese", "turkish",
        "ukrainian", "vietnamese", None]

    click id "pref_btn" until screen "preferences"
    click id "pref_general_btn" until id f"pref_change_language_btn_{lang}"
    click id f"pref_change_language_btn_{lang}"

    click "Options" raw
    click "Theme" raw
    click "Install Libraries" raw
    click "Actions" raw
    click "Lint" raw
    click id "return_btn" until screen "front_page"

testcase themes:
    click id "pref_btn" until screen "preferences"

    click id "pref_theme_btn" until "Default Theme" raw
    click id "pref_theme_dark_btn"
    click id "pref_theme_btn" until "Default Theme" raw
    click id "pref_theme_default_btn"
    # click id "pref_theme_btn"
    # click id "pref_theme_dark_btn"

    click id "return_btn" until screen "front_page"


testsuite default:
    setup:
        python:
            import shutil
            import tempfile

            persistent.old_projects_directory = persistent.projects_directory

            if persistent.temp_projects_directory:
                if os.path.exists(persistent.temp_projects_directory):
                    shutil.rmtree(persistent.temp_projects_directory)

                os.mkdir(persistent.temp_projects_directory, 0o777)
            else:
                persistent.temp_projects_directory = tempfile.mkdtemp(prefix="renpy-test-")

            persistent.projects_directory = persistent.temp_projects_directory

    before testcase:
        $ _test.timeout = 10.0

    teardown:
        python:
            persistent.projects_directory = persistent.old_projects_directory
            if os.path.exists(persistent.temp_projects_directory):
                shutil.rmtree(persistent.temp_projects_directory)

            persistent.temp_projects_directory = None


    testcase new_project:
        $ _test.timeout = 15.0
        click "refresh"
        click "Create New Project" until not screen "front_page"

        # Name
        click id "continue_btn" until id "input"
        click id "continue_btn" until not id "input"
        click id "return_btn" until id "input"
        type "Test Project"
        click id "continue_btn" until "1280x720"

        # Size
        click "1280x720"
        click id "continue_btn" until screen "choose_gui_color"

        # Color Selection
        click id "continue_btn" until not screen "choose_gui_color"
        pause until screen "front_page"


    testsuite translate_project:
        before testcase:
            if not screen "front_page":
                run Show("front_page")

            $ _test.timeout = 10.0
            click "Generate Translations" until not screen "front_page"

        testcase piglatin:
            keysym "K_BACKSPACE" repeat 30
            type "piglatin"
            click "Generate Translations" until not screen "translate"
            click id "continue_btn" until screen "front_page"

        testcase extract:
            click "Extract String Translations" until not screen "translate"
            click id "continue_btn" until screen "front_page"

        testcase merge:
            click "Merge String Translations" until not screen "translate"
            click id "continue_btn" until screen "front_page"

        testcase update:
            click "Update Default Interface Translations" until not screen "translate"
            pause until screen "front_page"


    testsuite extract_dialogue:
        before testcase:
            click "Extract Dialogue" until screen "extract_dialogue"
            click "Strip text tags"
            click "Escape quotes"
            click "Extract all"

        testcase tab_delimited:
            click "Tab-delimited"
            click id "continue_btn" until screen "front_page"

        testcase text_only:
            click "Text Only"
            click id "continue_btn" until screen "front_page"

    testcase delete_persistent:
        click "Delete Persistent" until not screen "front_page"
        pause until screen "front_page"

    testcase recompile:
        click "Force Recompile" until not screen "front_page"
        pause until screen "front_page"

    testcase choose_colors:
        click "Change/Update GUI" until not screen "front_page"
        click "Choose new colors"
        click id "continue_btn" until screen "choose_gui_color"
        click id "continue_btn" until screen "front_page"

        click "Change/Update GUI" until not screen "front_page"
        click "Regenerate the"
        click id "continue_btn" until screen "front_page"

    testcase build_project:
        $ _test.timeout = 180.0

        click "Build Distributions" until screen "build_distributions"
        click id "build_btn" until not screen "build_distributions"
        pause until id "return_btn"
        click id "return_btn" until screen "front_page"


testcase android:
    enabled False

    $ _test.timeout = 60.0
    $ _test.maximum_framerate = False

    click "Tutorial"
    pause 0.5
    click "Android"

    # Download and install RAPT.
    if "Yes":

        click "Yes"
        click "Proceed"

    click "Install SDK"
    click "Yes" until "Continue"

    # We have to create the key.
    if "Cancel":
        type "Test Key"
        click id "continue_btn"
        click id "continue_btn"

    # Configure the application.
    click "Configure"

    $ _test.maximum_framerate = True

    keysym "K_BACKSPACE" repeat 30
    type "Ren'Py Tutorial"
    click id "continue_btn"

    keysym "K_BACKSPACE" repeat 30
    type "Ren'Py Tutorial"
    click id "continue_btn"

    keysym "K_BACKSPACE" repeat 30
    type "org.renpy.tutorial"
    click id "continue_btn"

    keysym "K_BACKSPACE" repeat 30
    type "1.2.3"
    click id "continue_btn"

    keysym "K_BACKSPACE" repeat 30
    type "10203"
    click id "continue_btn"

    $ _test.maximum_framerate = False

    click "In landscape"
    click id "continue_btn"

    click "Neither"
    click id "continue_btn"

    click "No."
    click id "continue_btn"

    click "Android 4.0"
    click id "continue_btn"

    # Access the internet.
    click "No"
    click id "continue_btn"

    # Build the package.
    click "Build Package"
    click id "continue_btn"
