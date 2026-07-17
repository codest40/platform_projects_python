from project.searchers.questions_process import QUESTIONS
from project.formatters.process import load_process_inventory_from_logs


def run_search(question, inventory, **kwargs):
    entry = QUESTIONS.get(question)
    if entry is None:
        raise ValueError(f"Unknown question: {question}")
    return entry["executor"](inventory, **kwargs)


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
    except Exception as e:
      return(f"ERROR: Try Again. Pick one number Only")

    kwargs = {}
    if question == "process":
        kwargs["pid"] = int(input("PID: "))
    result = run_search(
        question,
        inventory,
        **kwargs,
    )

    return result


def start(event_type="analysis"):
    inventory = load_process_inventory_from_logs(event_type)

    if inventory is None:
        print("No process inventory found.")
        return

    answer = interactive_process_search(inventory)
    print(answer)
    #print_answer(answer)


start()
