import anvil.server

@anvil.server.callable
def task_killer(task):
    task.kill()
    print("task killed")