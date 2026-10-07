# Rows loaded once at startup. Same order every time, so the ids stay put.
# A restart clears anything posted on top and loads this set again.


def load_fixtures(user_service, profile_service, game_service) -> None:
    ada = user_service.create_user("Ada")
    ben = user_service.create_user("Ben")
    cleo = user_service.create_user("Cleo")
    dan = user_service.create_user("Dan")

    for user in (ada, ben, cleo, dan):
        profile_service.create_profile(user.id, user.name)

    # Ada (X) vs Ben (O). Mid-game. Next mark is O.
    mid = game_service.create_game(ada.id, ben.id)
    for cell in (0, 1, 4):
        game_service.move(mid.id, cell)

    # Cleo (X) vs Dan (O). Empty board a client can play.
    game_service.create_game(cleo.id, dan.id)

    # Ada (X) vs Cleo (O). X wins on 0, 4, 8.
    won = game_service.create_game(ada.id, cleo.id)
    for cell in (0, 1, 4, 2, 8):
        game_service.move(won.id, cell)

    # Dan (X) vs Ada (O). O wins on 2, 4, 6.
    lost = game_service.create_game(dan.id, ada.id)
    for cell in (0, 2, 1, 4, 3, 6):
        game_service.move(lost.id, cell)

    # Ben (X) vs Dan (O). Full board, no line.
    drawn = game_service.create_game(ben.id, dan.id)
    for cell in (0, 1, 2, 4, 3, 5, 7, 6, 8):
        game_service.move(drawn.id, cell)
