from flask import Flask, request, redirect
from onelogin.saml2.auth import OneLogin_Saml2_Auth

app = Flask(__name__)

def prepare_request(request):
    return {
        'http_host': request.host,
        'script_name': request.path,
        'server_port': request.environ.get('SERVER_PORT'),
        'get_data': request.args.copy(),
        'post_data': request.form.copy(),
    }

@app.route('/')
def index():
    return '<a href="/login">Login SAML</a>'

@app.route('/login')
def login():
    req = prepare_request(request)
    auth = OneLogin_Saml2_Auth(req)
    return redirect(auth.login())

@app.route('/acs', methods=['POST'])
def acs():
    req = prepare_request(request)
    auth = OneLogin_Saml2_Auth(req)
    auth.process_response()
    return "SAML LOGIN OK"

app.run(host="0.0.0.0", port=5001)
