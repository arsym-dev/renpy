testsuite global:
    setup:
        $ _test.timeout = 2.0
        $ _test.transition_timeout = 0.05

    before testcase:
        if not screen "main_menu":
            run MainMenu(confirm=False)

    teardown:
        exit


testcase bad_end:
    run Start()
    advance until screen "choice"
    click "ask her later" until not screen "choice"
    advance until screen "main_menu"

testcase good_end:
    run Start()
    advance until "ask her right away"
    click "ask her right away" until not screen "choice"
    advance until ("an interactive book" or "video game")
    assert not "video game" ## Last condition fails since it's "videogame" in script
    assert "videogame"
    click "an interactive book" until not screen "choice"
    advance until screen "main_menu"

testcase history_screen_from_quick_menu:
    click "Start" until not screen "main_menu"

    # Open and close history using mouse
    click "History" until screen "history"
    pause 0.5
    click "Return" until not screen "history"

    # Open and close history using keysyms
    keysym "K_RETURN" "History"
    pause 0.5
    keysym "game_menu"

    assert not screen "history"
