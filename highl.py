#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# From https://raw.githubusercontent.com/solusipse/fiche/master/extras/lines/lines.py
# Modified by kmahyyg, Originally written by solusipse
# Licensed under MIT

from flask import Flask, abort, redirect
app = Flask(__name__)

import os, pygments, json
from pygments import highlight
from pygments.lexers import guess_lexer
from pygments.formatters import HtmlFormatter

cus_json = json.loads(open("/data/config.json",'r').read())

if cus_json['https_enabled'] == True:
    domain_prefix = "https://"
else:
    domain_prefix = "http://"

custom_port = 8988
custom_domain = domain_prefix + cus_json["baseurl"]
root_dir = cus_json["codepath"]


@app.route('/')
def main():
    return redirect(custom_domain, code=302)


@app.route('/<slug>/')
@app.route('/<slug>')
def beautify(slug):
    # Return 400 in case of urls longer than 64 chars
    if len(slug) > 64:
        abort(400)

    # Create path for the target dir
    target_dir = os.path.join(root_dir, slug)

    # Block directory traversal attempts
    if not target_dir.startswith(root_dir):
        abort(403)

    # Check if directory with requested slug exists
    if os.path.isdir(target_dir):
        target_file = os.path.join(target_dir, "index.txt")
        
        # File index.txt found inside that dir
        with open(target_file, "r", encoding="utf-8") as f:
            code = f.read()
            # Identify language
            lexer = guess_lexer(code)
            # Create formatter with line numbers
            formatter = HtmlFormatter(linenos=True, full=True)
            # Return parsed code
            return highlight(code, lexer, formatter)

    # Not found
    abort(404)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=custom_port)
