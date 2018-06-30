import libtcodpy as libtcod


def render_all(con, objects, game_map, screen_width, screen_height, colors):
    # Draw all the tiles in the game map
    for y in range(game_map.height):
        for x in range(game_map.width):

            if game_map.tiles[x][y].blocked:
                libtcod.console_set_char_background(con, x, y, colors.get('dark_wall'), libtcod.BKGND_SET)
            else:
                libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)
                
    # Draw all entities in the list
   

    if (len(objects['players']) != 0):
        for player in objects['players']:
            draw_entity(con,player)


    if (len(objects['bullets']) !=0):
        for bullet in objects['bullets'][:]:
            for _ in range(2):
                if(bullet.wall_collide() or bullet.move(objects['enemies'])):
                    clear_entity(con, bullet)
                    objects['bullets'].remove(bullet)
                else:    
                    draw_entity(con,bullet)

    if (len(objects['enemies']) != 0):
        for enemy in objects['enemies'][:]:
            if(enemy.wall_collide() or enemy.move(objects['players'],objects['bullets'])):
                if enemy.hp <1:
                    clear_entity(con, enemy)
                    objects['enemies'].remove(enemy)
            else:
                enemy.update_color()
                draw_entity(con,enemy)

        

    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)




def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity):
    libtcod.console_set_default_foreground(con, entity.color)
    libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)


def clear_entity(con, entity):
    # erase the character that represents this object
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)