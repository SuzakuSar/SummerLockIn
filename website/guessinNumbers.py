from flask import Blueprint, render_template


guessNum = Blueprint('guessNum', __name__)

@guessNum.route('/guessnumbers/')
def guess_Num():
    return render_template('guessinNumbers.html')