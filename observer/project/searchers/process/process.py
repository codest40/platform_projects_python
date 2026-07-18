from project.searchers.process.questions_process import QUESTIONS
from project.extractors.process import load_process_inventory_from_logs


def run_search(question, inventory, **kwargs):
    entry = QUESTIONS.get(question)
    if entry is None:
        raise ValueError(f"Unknown question: {question}")

    result = entry["executor"](
        inventory,
        **kwargs,
    )
    return result, entry["formatter"]


def list_questions():
    keys = list(QUESTIONS)
    for index, key in enumerate(keys, start=1):
        print(f"{index}. {QUESTIONS[key]['question']}")
    return keys


def interactive_process_search(inventory):
    keys = list_questions()
    try:
        choice = int(input("\nSelect a question: "))
        question = keys[choice - 1]
    except Exception:
        print("ERROR: Try Again. Pick one number only.")
        return None, None

    kwargs = {}
    if question == "process":
        kwargs["pid"] = int(input("PID: "))
    result, formatter = run_search(
        question,
        inventory,
        **kwargs,
    )
    return result, formatter


def print_answer(result, formatter):
    print(formatter(result))

def start(event_type="analysis"):
    inventory = load_process_inventory_from_logs(event_type)
    if inventory is None:
        print("No process inventory found.")
        return
    answer, formatter = interactive_process_search(inventory)

    if answer is None:
        return
    print_answer(
        answer,
        formatter,
    )


start()
