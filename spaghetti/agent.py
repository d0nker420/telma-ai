from tools import AddClass, EndConversation, ShowClasses, node_descriptions
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_openai import ChatOpenAI
import getpass
import os
import openai

API_KEY = os.environ.get('OPENAI_API_KEY')


llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

#Create a conversation flow for a restaurant reservation system using the following node types. The user should be greeted, asked for the number of people in their party, asked for the reservation time, and then given a confirmation message.

node_descriptions = {
    "YesNoConfirmationNode": {
        "description": "Asks a yes/no question and directs the flow based on the user's response. It can handle 'yes' and 'no' answers differently, routing to different nodes depending on the response.",
        "params": {
            "question": "Do you want to make a reservation?",
            "yes_alternatives": ["yes", "sure"],
            "no_alternatives": ["no", "nope"]
        },
        "handlers": {
            "on_yes": "ask_date",
            "on_no": "end"
        }
    },
    "OpenQuestionNode": {
        "description": "Collects open-ended input from the user based on a specific question. This is useful for gathering more detailed responses that aren't binary.",
        "params": {
            "question": "For how many people should we reserve the table?",
            "acknowledgment_prompt": "Got it, a table for {response}."
        },
        "handlers": {
            "node_exit": "confirm_reservation"
        }
    },
    "PromptNode": {
        "description": "Displays a simple message to the user and typically moves the conversation forward. It is used primarily for providing information or confirming actions.",
        "params": {
            "prompt": "Your reservation is confirmed. We look forward to seeing you!"
        },
        "handlers": {
            "node_exit": "end"
        }
    }
}

def setup_initial_context():

    # Node descriptions, encapsulating the logic and functionality of each node type
    node_descriptions = {
        "OpenQuestionNode": {
            "description": "Collects open-ended input from the user.",
            "params": {
                "question": "For how many people should we reserve the table?",
                "acknowledgment_prompt": "The response to the user"
            },
            "handlers": {
                "node_exit": "confirm_reservation"
            }
        },
        "PromptNode": {
            "description": "Displays a message and moves the conversation forward.",
            "params": {
                "prompt": "The text that will be displayed"
            },
            "handlers": {
                "node_exit": "end"
            }
        }
    }

    # Formatting node descriptions for the initial prompt
    formatted_node_descriptions = "\n\n".join([
        f"{node_type}: {details['description']} "
        f"Parameters: {', '.join([f'{param} - {desc}' for param, desc in details['params'].items()])} "
        f"Handlers: {', '.join([f'{handler} - {action}' for handler, action in details['handlers'].items()])}"
        for node_type, details in node_descriptions.items()
    ])

    initial_prompt = f"""
    You are an assistant in developing bots. Your goal is to take input from the user to understand their needs and then use the tools and node descriptions to generate a list of how the conversation will flow. Here are the node descriptions:
    {formatted_node_descriptions}
    """

    return initial_prompt

def user_interaction_for_nodes(initial_prompt):
    # User input to request specific node constructions
    #user_query = input("Please describe the conversation flow you'd like to create: ")
    user_query = "Restaurant reservation"

    # Generate conversation flow using OpenAI's Completion API
    response = openai.chat.completions.create(
        messages=[
            {"role": "system", "content": hidden_prompt},
            {"role": "system", "content": user_query}
            ],
        model="gpt-3.5-turbo-0125",
        max_tokens=1000
    )

    print(response.choices[0].message.content)

initial_prompt = setup_initial_context()
user_interaction_for_nodes(initial_prompt)
