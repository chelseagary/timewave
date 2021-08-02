# Contains functions relevant to speed mechanics in Timewave


def movespeed(move):
    # the more the ship moves, the faster obstacles/power-ups will move. This decays if ship doesnt move
    # Returns negative offset for progression function
    if move:
        return -.25
    else:
        return .05


def progression(ticks, offset):
    # As the game continues, the speed of objects will naturally increase. Pass in pygame.time.get_ticks()
    # Offset comes from picking up power-ups to slow time, should be 0 at game start
    # After the first 15 seconds, the speed of the meteors increases exponentially
    # Returns (X,Y)
    if ticks < 100:
        return 3, 2
    else:
        return (ticks * 1.01)/5000 - offset, (ticks * 1.009)/5000 - offset


def slowdown(offset):
    # Power-up that allows for objects to slow down, moving progression back
    return offset - (offset/4)


def takehit():
    # Slows ship movement speed with object hits it
    pass