import pickle


conversation_data = []


def load_conversation_data():
    global conversation_data
    try:
        with open('conversation_data.pkl', 'rb') as f:
            conversation_data = pickle.load(f)
    except FileNotFoundError:
        conversation_data = []


load_conversation_data()    


def save_conversation_data():
    with open('conversation_data.pkl', 'wb') as f:
        pickle.dump(conversation_data, f)


while True:
    print(f"Current conversation data: {conversation_data}")
    user_input = input("Enter a message (or 'quit' to exit): ")
    if user_input.lower() == 'quit':
        break
    conversation_data.append(user_input)
    save_conversation_data()
