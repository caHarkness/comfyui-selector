import websocket
import uuid
import json
import requests
import io
import aiohttp
import asyncio

from lib.helpers import *

from urllib.request import urlopen as urlopen
from urllib.parse import urlencode as urlencode

# From the supplied addresses, return the ComfyUI installation with the smallest queue:
async def get_least_busy_address(server_addresses):
    async with aiohttp.ClientSession() as s:
        address_selection   = None
        selection_score     = None

        for a in server_addresses:
            if address_selection is None:
                address_selection = a

            try:
                async with s.get(f"http://{a}/queue") as response:
                    text            = await response.text()
                    response_json   = json.loads(text)

                score = len(response_json["queue_running"]) + len(response_json["queue_pending"])

                if selection_score is None or score < selection_score:
                    address_selection   = a
                    selection_score     = score
            except:
                continue

        return address_selection

async def get_outputs_2(server_address, workflow_json):
    client_id = str(uuid.uuid4())
    prompt_id = None

    async with aiohttp.ClientSession() as s:

        # Submit the prompt to the ComfyUI server:
        async with s.post(
            f"http://{server_address}/prompt",
            json = {
                "prompt":       workflow_json,
                "client_id":    client_id
            }) as response:
            text            = await response.text()
            response_json   = json.loads(text)
            prompt_id       = response_json["prompt_id"]

        # Keep waiting for the history to have data:
        while True:
            history_address = f"http://{server_address}/history/{prompt_id}"

            async with s.get(history_address) as response:
                text            = await response.text()
                response_json   = json.loads(text)

            if not response_json:
                print("Sleeping...")
                time.sleep(1)
                continue
            break

        history         = response_json[prompt_id]
        output_images   = {}

        for o in history["outputs"]:
            for node_id in history["outputs"]:
                node_output = history["outputs"][node_id]
                files_output = []

                if "images" in node_output:
                    for image in node_output["images"]:
                        #image_data = get_output(image["filename"], image["subfolder"], image["type"], server_address)

                        url_params = urlencode({
                            "filename":     image["filename"],
                            "subfolder":    image["subfolder"],
                            "type":         image["type"]
                        })

                        output_address = f"http://{server_address}/view?{url_params}"
                        async with s.get(output_address) as response:
                            text = await response.read()

                        files_output.append({"data": text, "type": "image"})

                if "audio" in node_output:
                    for audio in node_output["audio"]:
                        #image_data = get_output(image["filename"], image["subfolder"], image["type"], server_address)

                        url_params = urlencode({
                            "filename":     audio["filename"],
                            "subfolder":    audio["subfolder"],
                            "type":         audio["type"]
                        })

                        output_address = f"http://{server_address}/view?{url_params}"
                        async with s.get(output_address) as response:
                            text = await response.read()

                        files_output.append({"data": text, "type": "image"})

                output_images[node_id] = files_output

    return output_images

