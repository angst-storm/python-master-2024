import dramatiq

@dramatiq.actor
def print_actor(message):
    print(f"Actor: {message}")