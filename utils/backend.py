def retreive_all_threads(checkpointer, user_id):
    """Return only the thread ids that belong to the given user.

    Thread ids are namespaced as ``"<user_id>::<uuid>"`` (see
    ``generate_thread_id``), so we filter the shared checkpoint store by that
    prefix to keep each user's conversations private.
    """
    all_threads = set()
    prefix = f"{user_id}::"

    for checkpoint in checkpointer.list(None):
        thread_id = checkpoint.config["configurable"]["thread_id"]
        if thread_id.startswith(prefix):
            all_threads.add(thread_id)

    return list(all_threads)
