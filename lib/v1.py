from config import *

import threading
import os
import os.path
import io
import asyncio
import time
import json

import lib.log as log

from lib.log import colors
from lib.helpers import *
from lib.request import Request

from app import flask_app
from flask import render_template

#from flask import Flask
from flask import request
from flask import make_response

stubs = {}

@flask_app.post("/v1/stub")
async def v1_stub_POST():
    stub_timestamp  = time.monotonic_ns()
    o               = request.json

    print(json.dumps(o))

    req = Request.create({
        "category":         o["category"],
        "channel_topic":    o["channel_topic"],
        "user_message":     o["user_message"],
        "user_roles":       o["user_roles"],
        "user":             o["user"],
        "all_options": {}
    })

    req.get_options_json()
    req.parse_input()
    req.get_workflow_json()

    result = {}

    if req.has_workflow_json_file():
        result["stub"]              = stub_timestamp
        result["all_options"]       = req.all_options
        stubs[f"{stub_timestamp}"]  = req

    print(json.dumps(result))

    resp = make_response(result, 200)
    resp.headers = {
        "Content-Type": "application/json"
    }

    return resp

@flask_app.post("/v1/process")
async def v1_process_POST():
    o               = request.json
    stub_timestamp  = o["stub"]
    req             = stubs[f"{stub_timestamp}"]

    req.get_options_json()
    req.parse_input()

    print("-----")
    print(req.all_options)
    print("-----")

    '''

    print(req.all_options["repeat_n_times"])
    print("---")
'''

    repeat_n_times = 1
    if "repeat_n_times" in req.all_options:
        repeat_n_times = req.all_options["repeat_n_times"]

    result = {
        "server_address":   "",
        "output_files":     [],
        "execution_time":   0.0
    }



    for i in range(repeat_n_times):
        req.get_workflow_json()

        output = await req.get_outputs()

        result["server_address"] = output["server_address"]
        result["execution_time"] = result["execution_time"] + output["execution_time"]

        for o in output["output_files"]:
            result["output_files"].append(o)

    result["all_options"] = req.all_options

    if "zip_files" in req.all_options and req.all_options["zip_files"] == True:
        file_paths  = []
        last_path   = ""

        for i in range(len(result["output_files"])):
            last_path = result["output_files"][i]["file_path"]
            file_paths.append(last_path)

        last_path   = re.sub(r"\.[A-Za-z0-9]{1,}$", ".zip", last_path)
        zip_command = f"zip -j {last_path}"

        for path in file_paths:
            zip_command = f"{zip_command} {path}"

        os.system(zip_command)

        last_path               = re.sub(r"^static\/", "", last_path)
        result["output_files"]  = f"{PUBLIC_ADDRESS}{last_path}"
    else:
        # Convert all the file_data objects to base64 for use inside a JSON string:
        for i in range(len(result["output_files"])):
            file_data = result["output_files"][i]["file_data"]
            file_path = result["output_files"][i]["file_path"]
            result["output_files"][i]["file_data"] = base64.b64encode(file_data).decode("utf-8")
            result["output_files"][i]["file_link"] = f"{PUBLIC_ADDRESS}{file_path}"

    resp = make_response(result, 200)
    resp.headers = {
        "Content-Type": "application/json"
    }

    # Remove the key we no longer need:
    if f"{stub_timestamp}" in stubs:
        del stubs[f"{stub_timestamp}"]

    return resp

@flask_app.post("/v1/save_session/<session_name>")
async def v1_save_session_sn_POST(session_name):
    o           = request.json
    file_path   = f"config/sessions/{session_name}.json"
    existing    = read_json(file_path, {})

    for k in ["category", "channel_topic", "user", "user_roles"]:
        if k in o:
            existing[k] = o[k]

    write_file(file_path, json.dumps(existing))

    resp = make_response({"success": True}, 200)
    resp.headers = {
        "Content-Type": "application/json"
    }

    return resp
