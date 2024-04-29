import uuid
import configparser

from datetime import datetime
from langchain.output_parsers import ResponseSchema


config = configparser.ConfigParser()
config.read('config.ini')


# TODO - create cmb schema for yesnoreponse for branching conversations
def get_cmb_schema(params, node_exit, node_type, id):
    return {id:
        {
            "type": node_type,
            "params": params,
            "handlers": {"node_exit": node_exit},
        }
    }


def get_yesno_cmb_schema(id, params, node_exit, on_no, node_type):
    return {id:
        {
            "type": node_type,
            "params": params,
            "handlers": {"node_exit": node_exit,
                     "on_no": on_no},
        }
    }


prompt_response_schema = {
    "type": "object",
    "properties": {
        "prompt": {"type": "string"}
    },
    "required": ["prompt"],
    "additionalProperties": False
}
yesno_response_schema = {
    "type": "object",
    "properties": {
        "question": {"type": "string"},
        "prompt_yes_acknowledgment": {"type": "string"},
        "prompt_no_acknowledgment": {"type": "string"},
        "yes_alternatives": {
            "type": "array",
            "items": {"type": "string"}
        },
        "no_alternatives": {
            "type": "array",
            "items": {"type": "string"}
        },
        "node_exit": {
            "anyOf": [
                {"type": "string", "enum": ["end"]},
                {"type": "integer"}
            ]
        },
        "on_no": {
            "anyOf": [
                {"type": "string", "enum": ["end"]},
                {"type": "integer"}
            ]
        }
    },
    "required": ["question", "prompt_yes_acknowledgment", "prompt_no_acknowledgment", "yes_alternatives", "no_alternatives", "node_exit", "on_no"],
    "additionalProperties": False
}
openquestion_response_schema = {
    "type": "object",
    "properties": {
        "question": {"type": "string"},
        "acknowledgment_prompt": {"type": "string"}
    },
    "required": ["question", "acknowledgment_prompt"],
    "additionalProperties": False
}
smsmodule_response_schema = {
    "type": "object",
    "properties": {
        "prompt": {"type": "string"}
    },
    "required": ["prompt"],
    "additionalProperties": False
}
taskvalues_response_schema = {
    "type": "object",
    "properties": {
        "task_values": {
            "type": "object",
            "additionalProperties": {
                "type": "string"
            }
        }
    },
    "required": ["task_values"],
    "additionalProperties": False
}
numeric_rating_module_schema = {
    "type": "object",
    "properties": {
        "prompt": {"type": "string"},
        "out_of_bounds_prompt": {"type": "string"},
        "found_prompt": {"type": "string"},
        "try_again_prompt": {"type": "string"},
        "max_retries_reached_prompt": {"type": "string"}
    },
    "required": ["prompt", "out_of_bounds_prompt"],
    "additionalProperties": False
}


def get_schema_dict(node_type):
    schema = {
        "Prompt": prompt_response_schema,
        "OpenQuestion": openquestion_response_schema,
        "NumericRatingModule": numeric_rating_module_schema,
        "YesNoConfirmation": yesno_response_schema,
        "SMSModule": smsmodule_response_schema,
        }
    return schema[node_type]


def get_bot_schema(modules, task_values):
    root_module = next(iter(modules.keys()))
    bot_id = str(uuid.uuid4())
    return {
        "id": bot_id,
        "created at": datetime.now().isoformat(),
        "account_id": config["BOT"]["account_id"],
        "current_bot_version_id": config["BOT"]["current_bot_version_id"],
        "current_bot_version": {
            "id": str(uuid.uuid4()),
            # We need to fetch this metadata but for now itll be datetime.now()
            "created_at": datetime.now().isoformat(),
            "name": "",
            "description": "",
            # We should use english for the demo in the presentation
            "language": "en",
            "channel": "voice",
            "dialog": {
                "modules": modules,
                "root_module": root_module,
                "initial_user_response_timeout": config["BOT"]["initial_user_response_timeout"],
                },
            "omnichannel_config": {
                "voice": {
                    "initial_user_response_timeout": config["BOT"]["initial_user_response_timeout"],
                    "tts": {
                        "language": "en-GB",
                        "provider": config["BOT"]["provider"],
                        "voice": config["BOT"]["voice"],
                        # wtf is prosody
                        "prosody": {
                            "rate": "{}%".format(config["BOT"]["prosody"])
                            }
                        },
                    "stt": {
                        "language": "en-GB"
                        }

                    }
                },
            # idk what the two values below do ngl
            "mchannels_bot_id": "maria-cmb",
            # In the json it's true so make sure it converts correctly
            "permanent": True,
            # TODO - generate task_values by the AI as well
            "task_values": task_values,
            "bot_id": bot_id,
            },
        "labels": [],
        }
