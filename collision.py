def hit_self(snake_head, snake_parts):
    for snake_part in snake_parts:
        if snake_part.on_screen and \
            snake_head.snake_part.colliderect(
                snake_part.snake_part):
            return True

    return False

def hit_border(snake_head, level_width, level_height):
    # Test to see if the snake ran into a border
    if snake_head.snake_part.x < 0 or \
        (snake_head.snake_part.x +
         snake_head.snake_part.width) > (level_width + 1) or \
        snake_head.snake_part.y < 0 or \
        (snake_head.snake_part.y +
         snake_head.snake_part.height) > (level_height + 1) :
        return True

    return False


