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