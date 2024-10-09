import dramatiq

@dramatiq.actor
def run_actor(name, path):
    print(f"Run parser {name} by {path}")
    with open(path) as script:
        exec(script.read())