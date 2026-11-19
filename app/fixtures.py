# Rows loaded once at startup. Same order every time, so the ids stay put.
# A restart clears anything posted on top and loads this set again.


def load_fixtures(user_service, profile_service, history_service) -> None:
    ada = user_service.create_user("Ada")
    ben = user_service.create_user("Ben")
    cleo = user_service.create_user("Cleo")
    dan = user_service.create_user("Dan")

    profile_service.create_profile(
        ada.id, "Ada", "Plays the center square whenever it is free.", ["chess", "coding", "puzzles"]
    )
    profile_service.create_profile(
        ben.id, "Ben", "Prefers defensive play and aims for a draw.", ["music", "gaming", "cycling"]
    )
    profile_service.create_profile(
        cleo.id, "Cleo", "Fast player who always starts in a corner.", ["reading", "chess", "hiking"]
    )
    profile_service.create_profile(
        dan.id, "Dan", "New to Tic-Tac-Toe, learning opening traps.", ["cooking", "movies"]
    )

    # Ada (X) vs Cleo (O). X wins on 0, 4, 8.
    history_service.create_history(
        "Ada", "Cleo", ["X", "O", "O", "", "X", "", "", "", "X"], "Ada"
    )

    # Dan (X) vs Ada (O). O wins on 2, 4, 6.
    history_service.create_history(
        "Dan", "Ada", ["X", "X", "O", "X", "O", "", "O", "", ""], "Ada"
    )

    # Ben (X) vs Dan (O). Full board, no line.
    history_service.create_history(
        "Ben", "Dan", ["X", "O", "X", "X", "O", "O", "O", "X", "X"], "draw"
    )
