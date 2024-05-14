from llm_interface import call_language_model
from telma_ai import create_telma_graph
import json


def main():
    #user_input = input("Please describe the conversation flow you'd like to create: ")
    user_input = "silly goose dentist reservations for known customers"
    cmb_response = call_language_model(user_input)
    create_telma_graph(cmb_response, '8e207047-5344-4b62-89bc-6384229a51a5', 'd7624fa1-fb07-40e4-ba8b-a3324ce6accb')


if __name__ == "__main__":
    main()
