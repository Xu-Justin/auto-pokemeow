import utils

log = utils.logger()

def get_args_parser():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', action='store_true', help='Run iteration')
    parser.add_argument('--preview', action='store_true', help='Preview iteration')
    parser.add_argument('--config', type=str, default='config.json', help='Path to config.json')
    parser.add_argument('--output_panels', type=str, default=None, help='Path to store output panels')
    parser.add_argument('--output_color_panel', type=str, default=None, help='Path to store output color panel')
    args = parser.parse_args()
    return args

def iterate(input_panel, color_panel, colors, color_tolerance, balls, commands, args, **kwargs):

    if args.output_panels is not None:
        utils.get_preview_panels(input_panel, color_panel, balls).save(args.output_panels)
        log.info(f'saved panels to {args.output_panels}')

    if not args.preview:
        cord = utils.random_xy(*input_panel)
        utils.cursor.move(*cord, duration=utils.random.uniform(*kwargs['cursor_duration']))
        utils.cursor.left_click()
        utils.sleep(utils.random.uniform(*kwargs['sleep_after_move_cursor']))
        utils.keyboard.write(commands['pokemon'])
        utils.keyboard.enter()
        utils.sleep(utils.random.uniform(*kwargs['sleep_after_command']))

    color_image = utils.get_screen_image(*color_panel)
    if args.output_color_panel is not None:
        color_image.save(args.output_color_panel)
        log.info(f'saved color panel to {args.output_color_panel}')

    average_color = utils.average_image_color(color_image)
    color = utils.match_color(average_color, colors, color_tolerance)
    if color is None:
        return log.error(f'failed match_color with average_color : {average_color} and color_tolerance : {color_tolerance}')
    
    rarity = color
    ball = utils.match_ball(rarity, balls)
    if ball is None:
        return log.error(f'#failed match_ball with rarity : {rarity}')
    
    if not args.preview:
        cord = utils.random_xy(*ball.panel)
        utils.cursor.move(*cord, duration=utils.random.uniform(*kwargs['cursor_duration']))
        utils.cursor.left_click()

    log.info(f'catched pokemon with rarity : {rarity} and ball {ball.name}')

def main():
    args = get_args_parser()
    log.info(args) 

    cfg = utils.config.load(args.config)
    input_panel = utils.config.load_input_panel(cfg)
    color_panel = utils.config.load_color_panel(cfg)
    colors = utils.config.load_colors(cfg)
    color_tolerance = utils.config.load_color_tolerance(cfg)
    balls = utils.config.load_balls(cfg)
    commands = utils.config.load_commands(cfg)
    kwargs = utils.config.load_kwargs(cfg)

    log.info(f'input_panel : {input_panel}')
    log.info(f'color_panel : {color_panel}')
    for key, color in colors.items():
        log.info(f'color - {key} : {color}')
    log.info(f'color_tolerance : {color_tolerance}')
    for key, ball in balls.items():
        log.info(f'ball - {key} : {ball}')
    for key, command in commands.items():
        log.info(f'command - {key} : {command}')
    log.info(f'kwargs : {kwargs}')
    
    if args.run:
        try:
            while True:
                iterate(input_panel, color_panel, colors, color_tolerance, balls, commands, args, **kwargs)
                if not args.preview:
                    utils.sleep(utils.random.uniform(*kwargs['sleep_after_iteration']))
                if args.preview:
                    utils.sleep(kwargs['sleep_after_iteration_preview'])
        except KeyboardInterrupt:
            pass
        
if __name__ == '__main__':
    main()