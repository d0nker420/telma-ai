from llm_interface import call_language_model
from text_to_cmb import create_cmb_json
from telma_ai import create_telma_graph

def main():
    user_input = input("Please describe the conversation flow you'd like to create: ")
    llm_response = call_language_model(user_input)
    cmb_json = create_cmb_json(llm_response)
    web_page = create_telma_graph(cmb_json)
    print(f"The graph should be here: {web_page}")

if __name__ == "__main__":
    main()
