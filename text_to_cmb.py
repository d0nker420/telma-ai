import os
import copy
import uuid
import json
import configparser
import numpy as np

from jsonschema import validate
from jsonschema.exceptions import ValidationError
from openai import OpenAI
from schema import get_schema_dict, get_cmb_schema, get_yesno_cmb_schema, get_bot_schema


conversation_history = []

config = configparser.ConfigParser()
config.read('config.ini')

# Ensure OPENAI_API_KEY is defined in env and contains your api key, or put it in config.ini
#API_KEY = os.environ.get('OPENAI_API_KEY')
API_KEY = config['DEFAULT']['api_key']
MAX_TOKENS = int(config['DEFAULT']['max_tokens'])
HIDDEN_PROMPT = config['HIDDEN_PROMPTS']['hidden_prompt']
MODEL = "gpt-4-turbo-preview"
client = OpenAI()

# TODO - implement this code on the front end for telma locally with violentmonkey and that chat widget we were sent
# TODO - allow the user to continously edit the graph
with open('prompts/assemble_prompt.txt', 'r') as file:
    assemble_prompt = file.read().strip()

# user_query = input("Enter the conversation you'd like to create a bot for: ")
user_query = "silly goose orthodontics reservation bot"
conversation_prompt = HIDDEN_PROMPT + user_query

module_list = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": assemble_prompt},
        {"role": "user", "content": "Make the flow for a Pizza Hut reservation bot"},
        {"role": "assistant", "content": "1. Prompt //Greet the customer and tell them they called into Pizza hut 2. OpenQuestion //Ask about when the customer wishes to reserve a table for 2. OpenQuestion //Ask how many people will be at the table 3. Prompt //Thank the customer for making a reservation and say goodbye"},
        {"role": "user", "content": conversation_prompt}
        ],
    max_tokens=MAX_TOKENS
).choices[0].message.content

print(module_list)

with open('prompts/json_prompt.txt', 'r') as file:
    json_prompt = file.read().strip()

bot_cmb = json.loads(client.chat.completions.create(
    model=MODEL,
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": json_prompt},
        {"role": "system", "content": module_list},
        {"role": "user", "content": user_query},
        ],
    max_tokens=MAX_TOKENS
).choices[0].message.content)

with open('output.json', 'w') as f:
    json.dump(bot_cmb, f, indent=4)

print(bot_cmb)

nodes = np.array(["SMSModule", "YesNoConfirmation", "NumericRatingModule", "OpenQuestion", "Prompt"])
cmb_sorted = sorted(bot_cmb.keys(), key=lambda x: int(x[-1]))
nodes_sorted = []
for node_type in cmb_sorted:
    for node in nodes:
        if node in node_type:
            node_class = node
            nodes_sorted.append(node_class)
    schema = get_schema_dict(node_class)
    try:
        validate(instance=bot_cmb[node_type], schema=schema)
    except ValidationError as e:
        print("JSON data is invalid.")
        print("Validation Error:", e)
        print(node_class)

print("TESTS PASSED")

ids = [str(uuid.uuid4()) for i in range(len(cmb_sorted))]
modules = {}
for i, (id, node_type) in enumerate(zip(ids, cmb_sorted)):
    params = bot_cmb[node_type]
    if "YesNoConfirmation" in node_type:
        no_idx = params["on_no"]
        exit_idx = params["node_exit"]
        # These can be "end" as wel
        on_no = "end"
        node_exit = "end"
        if not no_idx == "end":
            on_no = ids[int(no_idx) - 1]
        if not exit_idx == "end":
            node_exit = ids[int(exit_idx) - 1]
        del bot_cmb[node_type]["on_no"]
        del bot_cmb[node_type]["node_exit"]

        modules.update(get_yesno_cmb_schema(id, params, node_exit, on_no, nodes_sorted[i]))

    node_exit = "end"
    if not i + 1 == len(ids):
        node_exit = str(ids[i + 1])

    modules.update(get_cmb_schema(params, node_exit, nodes_sorted[i], id))

cmb_output = get_bot_schema(modules, {})

with open('output.json', 'w') as f:
    json.dump(cmb_output, f, indent=4)
