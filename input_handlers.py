import libtcodpy as libtcod


def handle_keys(objects):
    key = libtcod.console_check_for_keypress()  #real-time
    #key = libtcod.console_wait_for_keypress(True)  #turn-based
 
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        #Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
 
    elif key.vk == libtcod.KEY_ESCAPE:
        return True  #exit game
    
    if libtcod.console_is_key_pressed(libtcod.KEY_SPACE):
        for player in objects['players']:
            player.shoot(objects['bullets'])
 
    #movement keys
    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        update_player(0,-1,'^',objects['players'])
 
    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        update_player(0,1,'v',objects['players'])
 
    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        update_player(-1,0,'<',objects['players'])
 
    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        update_player(1,0,'>',objects['players'])




def update_player(x,y,char,players):

    for player in players:
        player.move(x,y)
        player.char = char
