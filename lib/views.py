import os
import asyncio
import re

from lib.helpers import *

from flask import Flask
from munch import Munch
from munch import munchify
from markdown import markdown

from app import flask_app
from flask import render_template

def get_common_vars():
    common = Munch()

    sessions = []
    if os.path.isdir("config/sessions"):
        for s in os.listdir("config/sessions"):
            if re.match(r"^_", s):
                continue

            session_name    = re.search(r"(.+)\.json$", s).group(1)
            session_json    = read_json(f"config/sessions/{session_name}.json", {})
            session_json["session_name"] = session_name
            sessions.append(session_json)

    common.sessions = sessions
    return common

@flask_app.get("/sessions")
def sessions_GET():
    common = get_common_vars()
    return render_template("sessions.html", common=common)

@flask_app.get("/session/<session_name>")
def session_GET(session_name):
    common = get_common_vars()

    common.session_name     = session_name
    common.category         = ""
    common.channel_topic    = ""
    common.user             = ""
    common.user_roles       = ""

    session_json = read_json(f"config/sessions/{session_name}.json", {})

    for k in ["category", "channel_topic", "user", "user_roles"]:
        if k in session_json:
            common[k] = session_json[k]

    print(common.user)

    return render_template("session.html", common=common)

# Test the functionality of a ComfyUI instance
@flask_app.get("/test")
def test_GET():
    server_address  = "10.44.7.100:8188"
    client_id       = str(uuid.uuid4())

    json_data = read_json("workflow_api.json", "")
    json_data["3"]["inputs"]["seed"] = random.randint(1, 999999)

    p       = {"prompt": json_data}
    data    = json.dumps(p).encode("utf-8")
    req     =  request.Request(f"http://{server_address}/prompt", data=data)

    with request.urlopen(req) as resp:
        body = resp.read().decode("utf-8")

    print(body)

    body        = json.loads(body)
    prompt_id   = body["prompt_id"]


    while True:
    
        address = f"http://{server_address}/history/{prompt_id}"

        with request.urlopen(address) as resp:
            resp = json.loads(resp.read())

        if not resp:
            print("Sleeping...")
            time.sleep(1)
            continue

        break

    #print(resp)

    outputs = resp[prompt_id]["outputs"]

    # {'9': {'images': [{'filename': 'ComfyUI_01727_.png', 'subfolder': '', 'type': 'output'}]}}
    print(resp[prompt_id]["outputs"])

@flask_app.template_global()
def md(f_path):
    try:
        f_text = read_file(f_path, "")
        f_markdown = markdown(f_text)
        return f_markdown
    except Exception as x:
        print(x)
        return str(x)
