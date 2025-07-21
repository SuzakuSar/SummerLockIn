"""
Main Flask application initialization for SUMMERLOCKIN project
Registers all blueprints and configures the application
"""

from flask import Flask

def create_app():
    """
    Create and configure the Flask application
    """
    app = Flask(__name__)
    
    # Secret key for session management
    app.secret_key = 'shh_its_a_secret'
    
    # Configuration settings
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching during development
    
    # Import blueprints
    from .home import home
    from .helloWorld import helloWorld
    from .clicker_game.clicker_game import clicker_game
    from .random_jokes.random_jokes import random_jokes
    from .guessing_game.guessing_game import guessing_game
    from .hangman import hangman
    from .time_predict import time_predict
    from .space_memory import space_memory
    from .multiplication_trainer.multiplication_trainer import multiplication_trainer
    from .dino_runner.dino_runner import dino_runner
    from .snake_game.snake_game import snake_game
    from .tic_tac_toe.tic_tac_toe import tic_tac_toe
    from .rock_paper_scissors.rock_paper_scissors import rock_paper_scissors
    from .block_blast.block_blast import block_blast
    from .wordle import wordle
    from .typing_test.typing_test import typing_test
    from .click_speed.click_speed import click_speed
    from .drag_drop.drag_drop import drag_drop
    from .shell_game.shell_game import shell_game
    from .wire_matching.wire_matching import wire_matching
    from .do_not_click.do_not_click import do_not_click
    from .click_clear import click_clear
    from .number_sequence.number_sequence import number_sequence
    from .fake_download.fake_download import fake_download
    from .door_game.door_game import door_game
    from .fake_chatbot.fake_chatbot import fake_chatbot
    from .osu_game import osu_game
    from .lucky_lever.lucky_lever import lucky_lever
    from .tortoise_temp import tortoise_temp
    from .useless_fortune import useless_fortune
    from .bomb_defuse.bomb_defuse import bomb_defuse
    from .water_drinker.water_drinker import water_drinker
    from .space_invaders.space_invaders import space_invaders
    from .brick_breaker.brick_breaker import brick_breaker
    from .coin_flip.coin_flip import coin_flip
    from .i_spy import i_spy
    from .story_generator.story_generator import story_generator
    from .coordinate_game.coordinate_game import coordinate_game
    from .slider_challenge.slider_challenge import slider_challenge
    from .prank_helper.prank_helper import prank_helper
    from .pong import pong
    from .maze_game.maze_game import maze_game
    from .game_2048.game_2048 import game_2048
    from .balance_scale.balance_scale import balance_scale
    from .space_memory_game import space_memory_game
    from .connect_dots import connect_dots
    from .speed_sort.speed_sort import speed_sort
    from .lockpick_game.lockpick_game import lockpick_game
    from .one_pixel_hunt.one_pixel_hunt import one_pixel_hunt
    from .slots_machine.slots_machine import slots_machine

    # Register blueprints with URL prefixes
    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(helloWorld, url_prefix='/')
    app.register_blueprint(clicker_game, url_prefix='/clickergame')
    app.register_blueprint(random_jokes, url_prefix='/randomjokes')
    app.register_blueprint(guessing_game, url_prefix='/guessinggame')
    app.register_blueprint(hangman, url_prefix='/hangman')
    app.register_blueprint(time_predict, url_prefix='/timepredict')
    app.register_blueprint(space_memory, url_prefix='/spacememory')
    app.register_blueprint(multiplication_trainer, url_prefix='/mountainacademy')
    app.register_blueprint(dino_runner, url_prefix='/dino-runner')
    app.register_blueprint(snake_game, url_prefix='/snakegame') # fix
    app.register_blueprint(tic_tac_toe, url_prefix='/tictactoe')
    app.register_blueprint(rock_paper_scissors, url_prefix='/rockpaperscissors')
    app.register_blueprint(block_blast, url_prefix='/blockblast') # clean up
    app.register_blueprint(wordle, url_prefix='/wordle') # fix; submitted words labeled as "not a valid word"
    app.register_blueprint(typing_test, url_prefix='/typingtest') #doesn't work at all
    app.register_blueprint(click_speed, url_prefix='/clickspeed') # make start on click area
    app.register_blueprint(drag_drop, url_prefix='/dragdrop') # doesn't work
    app.register_blueprint(shell_game, url_prefix='/shellgame') #bro how tf can you track this sob
    app.register_blueprint(wire_matching, url_prefix='/wirematching')
    app.register_blueprint(do_not_click, url_prefix='/donotclick')
    app.register_blueprint(click_clear, url_prefix='/clickclear')
    app.register_blueprint(number_sequence, url_prefix='/numbersequence')
    app.register_blueprint(fake_download, url_prefix='/fakedownload')
    app.register_blueprint(door_game, url_prefix='/door')
    app.register_blueprint(fake_chatbot, url_prefix='/fakechatbot') # doesn't alternate properly
    app.register_blueprint(osu_game, url_prefix='/osu')
    app.register_blueprint(lucky_lever, url_prefix='/luckylever')
    app.register_blueprint(tortoise_temp, url_prefix='/tortoise_temp')
    app.register_blueprint(useless_fortune, url_prefix='/uselessfortune')
    app.register_blueprint(bomb_defuse, url_prefix='/bombdefuse') #error when cutting wire
    app.register_blueprint(water_drinker, url_prefix='/waterdrinker')
    app.register_blueprint(space_invaders, url_prefix='/space-invaders') #upon new wave everything freezes
    app.register_blueprint(brick_breaker, url_prefix='/brickbreaker')
    app.register_blueprint(coin_flip, url_prefix='/coinflip')
    app.register_blueprint(i_spy, url_prefix='/ispy')
    app.register_blueprint(story_generator, url_prefix='/storygenerator') # doesnt even appear
    app.register_blueprint(coordinate_game, url_prefix='/coordinategame')
    app.register_blueprint(slider_challenge, url_prefix='/slider_challenge') #doesnt work
    app.register_blueprint(prank_helper, url_prefix='/prankhelper')
    app.register_blueprint(pong, url_prefix='/pong')
    app.register_blueprint(maze_game, url_prefix='/maze') #errors
    app.register_blueprint(game_2048, url_prefix='/game2048')
    app.register_blueprint(balance_scale, url_prefix='/balancescale') # buggy
    app.register_blueprint(space_memory_game, url_prefix='/spacememorygame') #needs major fixing
    app.register_blueprint(connect_dots, url_prefix='/connect-dots') #needs more patterns
    app.register_blueprint(speed_sort, url_prefix='/speedsort')
    app.register_blueprint(lockpick_game, url_prefix='/lockpick')
    app.register_blueprint(one_pixel_hunt, url_prefix='/pixelhunt') # doesn't even appear
    app.register_blueprint(slots_machine, url_prefix='/slots') #buggy


    # Add any new blueprints here following the same pattern:
    # from .new_feature import new_feature
    # app.register_blueprint(new_feature, url_prefix='/newfeature')
    
    # Global context processor to make request available in all templates
    @app.context_processor
    def inject_request():
        """Make request object available in all templates for navigation highlighting"""
        from flask import request
        return dict(request=request)
    
    # Optional: Add custom error pages
    @app.errorhandler(404)
    def page_not_found(e):
        """Custom 404 page with space theme"""
        from flask import render_template
        return render_template('404.html'), 404
    
    # # Optional: Add custom template filters
    # @app.template_filter('star_emoji')
    # def star_emoji_filter(number):
    #     """Convert number to star emojis"""
    #     return '⭐' * min(int(number), 5)
    
    return app

# For development server
# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True)