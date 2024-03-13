def load_file(filename):
    with open(filename, "r") as file:
        return file.read()

    history_tutor_context = prompts.CONTEXT_HISTORY_TUTOR
    lister_and_carbolic_acid_context = load_file(
        "./history_tutor/lister_and_carbolic_acid.md"
    )
    history_tutor_context = history_tutor_context.replace(
        "%%CONTEXT%%", lister_and_carbolic_acid_context
    )
