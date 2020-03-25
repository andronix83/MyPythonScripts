import json
import re
import textwrap
from collections import namedtuple

import requests
from fake_useragent import UserAgent

BASE_URL = "https://app.sli.do/api/v0.5/events"
SLIDO_APP_VERSION = "SlidoParticipantApp/5.5.0 (web)"

USER_AGENT = UserAgent()


def handle_cancellation(input_item: str, stop_symbol="") -> str:
    if input_item == stop_symbol:
        print("Operation has been cancelled. Exit application.")
        exit(0)
    return input_item


def ask_for_event_tag() -> str:
    while True:
        event_tag = input("\nInput an event tag or the whole URL (or empty string to cancel): ")
        event_tag = handle_cancellation(event_tag.strip().lower())
        if event_tag.startswith("http") or event_tag.startswith("app.sli.do"):
            try:
                event_tag = re.search(r"/event/(.+?)/", event_tag).group(1)
                break
            except AttributeError:
                print("Incorrect URL! Try again!")
        else:
            break
    return event_tag


def check_response_status(resp: requests.models.Response) -> requests.models.Response:
    if not resp.ok:
        raise Exception(f"Incorrect request! (code={resp.status_code}, text={resp.text})")
    return resp


def resolve_event_uuid(event_tag: str) -> str:
    url = f"{BASE_URL}?hash={event_tag}"
    resp = check_response_status(requests.get(url))
    resp_json = resp.json()
    return resp_json[0]['uuid'] if resp_json else None


def auth_new_user(event_uuid: str) -> str:
    url = f"{BASE_URL}/{event_uuid}/auth"
    resp = check_response_status(requests.post(url))
    return resp.json()['access_token']


def create_http_headers(event_uuid: str) -> dict:
    return {
        "Authorization": f"Bearer {auth_new_user(event_uuid)}",
        "User-Agent": USER_AGENT.random,
        "x-slidoapp-version": SLIDO_APP_VERSION
    }


def retrieve_question_list(event_uuid: str) -> list:
    resp = check_response_status(requests.get(f"{BASE_URL}/{event_uuid}/questions",
                                              headers=create_http_headers(event_uuid)))
    return json.loads(resp.text, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))


def format_question(question, question_max_with=160) -> str:
    short_text = textwrap.shorten(question.text, width=question_max_with, placeholder='...?')
    return f"{question.event_question_id}: ({question.score}) - {short_text}"


def ask_for_chosen_question(questions: list):
    while True:
        question_id = input("\nInput selected question ID (at least, last 4 digits, or empty to cancel): ")
        question_id = handle_cancellation(question_id.strip())
        if len(question_id) < 4:
            print("Error: question ID is shorter than 4 digits! Try again!")
            continue
        try:
            return next(q for q in questions if
                        str(q.event_question_id).endswith(question_id) and not q.date_deleted)
        except StopIteration:
            print(f"Error: question with ID={question_id} not found! Try again!")


def ask_for_upvotes_count() -> int:
    while True:
        upvotes_count_str = input("\nInput the number of votes to add (or empty to cancel): ")
        upvotes_count_str = handle_cancellation(upvotes_count_str.strip())
        if not upvotes_count_str.isdigit():
            print("Error: number of votes is not a number (or negative)! Try again!")
            continue
        return int(upvotes_count_str)


def vote(question_id: str, event_uuid: str, upvote=True) -> int:
    resp = check_response_status(requests.post(f"{BASE_URL}/{event_uuid}/questions/{question_id}/like",
        json={
            'score': 1 if upvote else -1
        },
        headers=create_http_headers(event_uuid)
    ))
    return resp.json()['event_question_score']


def main() -> None:

    # 1. Ask user for event tag (or full URL) and resolve its event UUID
    while True:
        event_tag = ask_for_event_tag()
        # event_tag = "xfpxmqim"  # TODO: DELETE later!
        event_uuid = resolve_event_uuid(event_tag)
        if event_uuid:
            break
        else:
            print("Event tag can't be resolved! Try Again!")

    # 2. Load question list by resolved event UUID
    questions = retrieve_question_list(event_uuid)

    # 3. Print all the event questions for the user to choose from
    for question in questions:
        print(format_question(question, question_max_with=80))

    # 4. Ask user for chosen question ID and print this question
    chosen_question = ask_for_chosen_question(questions)
    print(format_question(chosen_question))

    # 5. Ask how many upvotes need to be added for the question
    upvotes_count = ask_for_upvotes_count()

    # 6. Upvoting process loop for the specified question
    print(f"\nStarting the upvoting process for {upvotes_count} votes:")
    for i in range(upvotes_count):
        total_score = vote(chosen_question.event_question_id, event_uuid)
        print(f" - Vote #{i+1}: successful (total score after the vote: {total_score})")
        # TODO: BUG - total score is always 1, despite the real count is changing


# Script entry point
if __name__ == '__main__':
    main()
