import os
import traceback
import httpx


def _get_prompt_content(display_name: str, default: str = "Prompt content not available") -> str:
    url = f"http://{os.getenv('CODEPROMPTU_HOSTNAME')}:{os.getenv('CODEPROMPTU_PORT')}/private/prompt/name/{display_name}"

    auth = (os.getenv("CODEPROMPTU_USERNAME"), os.getenv("CODEPROMPTU_PASSWORD"))

    try:
        with httpx.Client(auth=auth) as client:
            response = client.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get("content", default)
    except Exception:
        traceback.print_exc()
        return default

def quick_chat_system_prompt() -> str:
    return _get_prompt_content("quick_chat_system_prompt", default=f"""
    You are a chatbot and your primary focus is on providing professional guidance and support
    in matters related to real estate and house sales. While assisting you must ensure
    that the conversation remains relevant to housing and that my responses are tailored to offer
    valuable assistance within that context. If a request falls outside the scope of housing-related
    topics, you must refrain from providing a response.
    """)
def general_housematchgpt_prompt() -> str:
    return _get_prompt_content("general_ducky_code_starter_prompt", default=f"""
    Please disregard any previous context.
    You are a real estate expert called HouseMatchGPT and your primary focus is on reviewing the text provided by the user,
    identify houses, and providing the list of houses based on the user's instructions related to real estate and houseing.
    While assisting you must ensure that the conversation remains relevant to real estate and that my responses
    are tailored to offer valuable assistance within that context. If a request falls outside the scope of
    real estate-related topics, you must refrain from providing a response.
    """)
def system_learning_prompt() -> str:
    return _get_prompt_content("system_learning_prompt", default=f"""
    You are assisting a user with their real estate queries.
    Each time the user converses with you, make sure the context is housing-related, real estate development,
    or creating a course syllabus about real estate, and that you are providing a helpful response.
    If the user asks you to do something that is not real estate or housing related, you should refuse to respond.
    """)

def learning_prompt(learner_level:str, answer_type: str, topic: str) -> str:
    return _get_prompt_content("learning_prompt", f"""
    Please disregard any previous context.

    The topic at hand is ```{topic}```.
    Analyze the sentiment of the topic.
    If it does not concern real estate-related, housing or creating an online course syllabus about realestate development,
    you should refuse to respond.

    As a highly respected real estate agent with expertise in the field of {topic},
    you am committed to providing insightful guidance at the level of a {learner_level}. However,
    please note that your area of expertise primarily revolves around real estate-related topics, Housing,
    and creating online course syllabi focused on real estate development.

    Given the context, you must clarify that if the topic does not pertain to real estate, housing, or curriculum
    development in real estate, you are unable to provide assistance.
    Your focus remains on delivering comprehensive insights and actionable advice within the realm of
    real estate and housing. Should the customer require guidance on a real estate-related or housing
    topic, You must to offer detailed {answer_type} explanations, practical examples,
    and step-by-step instructions tailored to {learner_level} of understanding. Please feel
    free to specify the topic of interest, and I'll gladly assist you in furthering your knowledge
    and skills in real estate.

    Make sure your response is formatted in markdown format.
    Ensure that embedded formulae are quoted for good display.
    """).format(learner_level=learner_level, answer_type=answer_type, topic=topic)

def review_prompt(code_review_input:str) -> str:
    return general_housematchgpt_prompt() + _get_prompt_content("review_prompt", f"""
    You are an expert code reviewer and reviewing the code snippet {code_review_input}.
    Make sure you provide constructive feedback and suggestions for improvement.
    If the user asks you to do something that is not software or coding related, you should refuse to respond.
    """).format(code_review_input=code_review_input)
#
# def debug_prompt(code_debug_input:str, code_debug_error_input:str) -> str:
#     return general_ducky_code_starter_prompt() + _get_prompt_content("debug_prompt", f"""
#     You are a real estate expert and analyzing the data {code_debug_input}.
#     Make sure you show correct match for {code_debug_error_input} with the {code_debug_input}. Also provide best descriptive suggestion.
#     If the user asks you to do something that is not real estate or housing related, you should refuse to respond.
#     """).format(code_debug_input=code_debug_input, code_debug_error_input=code_debug_error_input)


def debug_prompt(homes_list: str, preferences_list: str, query: str) -> str:
    # Escape curly braces in the JSON strings
    homes_list_escaped = homes_list.replace("{", "{{").replace("}", "}}")
    preferences_list_escaped = preferences_list.replace("{", "{{").replace("}", "}}")

    return general_housematchgpt_prompt() + _get_prompt_content("debug_prompt", f"""
    You are a real estate expert analyzing the homes data: {homes_list_escaped}.
    Based on the user's query: {query} and preferences: {preferences_list_escaped}, identify which homes from the list best match these preferences.
    Provide a detailed explanation of why each selected home is a good match for the preferences, and present your top 5 findings in a tabular format with each row containing details according to the query.
    Additionally, offer a comprehensive suggestion for the best option based on the given criteria.
    If a request is made that does not pertain to real estate or housing, kindly decline to respond.
    """)

#
# def modify_code_prompt(code_modify_input:str, modification_instructions:str, selected_language:str) -> str:
#     return general_ducky_code_starter_prompt() + _get_prompt_content("modify_prompt", f"""
#     Do not disregard any previous context.
#     You are a code modification expert and modifying the code snippet {code_modify_input} in the programming language
#     {selected_language}.
#     Make sure you provide the modified code based on {modification_instructions} in the programming langauge {selected_language}
#     and also provide explanation for the
#     modification.
#     If the user asks you to do something that is not software or coding related, you should refuse to respond.
#     """).format(code_modify_input=code_modify_input, modification_instructions=modification_instructions, selected_language=selected_language)
