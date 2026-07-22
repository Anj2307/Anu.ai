def retreive_all_threads(checkpointer):
    all_threads = set()

    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config["configurable"]["thread_id"])

    return list(all_threads)
