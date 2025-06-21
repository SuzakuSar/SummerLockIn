from website import create_app
import time

from flask import Flask, render_template, url_for, request, jsonify, session, redirect, g



app = create_app()
app.secret_key = 'shh_its_a_secret'


@app.before_request
def log_request_info():
    """Log details about each request to help debug routing issues"""
    print("\n=== REQUEST INFO ===")
    print(f"URL: {request.url}")
    print(f"Path: {request.path}")
    print(f"Method: {request.method}")
    print(f"Endpoint: {request.endpoint}")
    print(f"Blueprint: {request.blueprint}")
    print("===================\n")

if __name__ == "__main__":
    app.run(debug=True)
