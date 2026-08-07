from .parent_node import Node
from app.state.joke_state import JokeState
from app.client.langchain_llm import LLM_Chain
from app.prompts.joke_prompt import get_joke_prompt
from langgraph.types import interrupt,Command

class Joke_Node(Node):

    def __init__(self,llm_client:LLM_Chain):
        self.llm_client=llm_client


    def check_condition(self,state:JokeState):

        if state['approved']=='yes':
            return 'yes'
        else:
            return 'no'


    def generate_joke(self,state:JokeState):

        topic=state['topic']
        previous_versions=state['previous_versions']

        print(f"-----PREVIOUS JOKES----{previous_versions}")

        values={'topic':topic,'previous_versions':previous_versions}

        response=self.llm_client.get_llm_chain_response(prompt=get_joke_prompt(),values=values)

        return {'current_joke':response}


    def approve_joke(self,state:JokeState):

        decision=interrupt({
            "type":"approval",
            "latest_joke":state['current_joke'],
            "question":"Did you like the joke? Type yes/no"
        })

        user_decision=decision['approval']

        prev_jokes=state['previous_versions'] 
        prev_jokes.append(state['current_joke'])

        if user_decision=='yes':
            return {'approved':user_decision,'previous_versions':prev_jokes,'final_joke':state['current_joke']}
        else:
            return {'approved':user_decision,'previous_versions':prev_jokes,'final_joke':"Not Finalized"}


    def get_all_nodes(self:JokeState):
        pass