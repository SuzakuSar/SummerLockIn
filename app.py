from website import create_app
import time

from flask import Flask, render_template, url_for, request, jsonify, session, redirect

app = create_app()
app.secret_key = 'shh_its_a_secret'


if __name__ == "__main__":
    app.run(debug=True)
