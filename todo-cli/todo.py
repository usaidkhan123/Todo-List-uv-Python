import click
import json
import os

TODO_FILE = 'todo.json'

def load_tasks():
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, 'r') as file:
        return json.load(file)
    
def save_tasks(tasks):                           # ye function json ki file me hamara data write mode me store krr raha hai
    with open(TODO_FILE, "w") as file:
        json.dump(tasks, file, indent=4)


@click.group()
def cli():
    """Simple Todo List Manager"""              # ye hamari help message hogi 
    pass

@click.command()
@click.argument('task')                         # task ko user se lega aur agge pass krde ga 
def add(task):         #hamari JSON file ke andar hamare data ko store krne ka kaam krr raha hai . task ko lega parameter ke tor parr aor put kardega hamari file me
    """Add a to the list new task"""
    tasks = load_tasks()                        # file ko open krlia hai add name ke function or store krdia hai task ke variable
    tasks.append({"task": task, "done":False})                              # json ki file ka structure define krr rahe hain jo append hoga json ki file me
    save_tasks(tasks)
    click.echo(f"Task '{task}' added to the list.")                         # task added to the list ki message print krr raha hai . echo aik print function hai jo print karata  hai

# list name ka function bana rahe hainn jo hamare todos terminal perr list list karega 
@click.command()
def list():
    """list all the task"""
    tasks = load_tasks()          # load karega sare task ko 
    if not tasks:
        click.echo("No Task Found")
        return
    for index, task in enumerate(tasks,1):                                              # enumerate loop krta hai har task ko  numbering ke sath
        status = "Done" if task["done"] else "Not Done"                                 # status ko define krrahe hain done or not done
        click.echo(f"{index}. {task['task']}  [{status}]")                                # task ko print krrahe hain   


@click.command()
@click.argument("task_number", type=int)                                               # task number ko user se lega
def complete(task_number):
    """Mark a task as complete"""
    tasks = load_tasks()
    if 0 < task_number <= len(tasks):
        tasks[task_number  - 1]["done"] = True
        save_tasks(tasks)
        click.echo(f"Task {task_number} marked as complete")
    else:
        click.echo(f"Invalid task number {task_number}")



@click.command()
@click.argument("task_number", type=int)
def remove(task_number):
    """Remove a task from list"""
    tasks =  load_tasks()
    if 0 < task_number <= len(tasks):
        removed_task = tasks.pop(task_number - 1)
        save_tasks(tasks)
        click.echo(f"Removed Task '{removed_task['task']}' removed from the list")
    else:
        click.echo(f"Invalid task number {task_number}")

cli.add_command(add)                            # add command ko add krr rahe hain cli me
cli.add_command(list)                           # list command ko add krr rahe hain cli me
cli.add_command(complete)                       # complete command ko add krr rahe hain cli me
cli.add_command(remove)                         # remove command ko add krr rahe hain cli me
if __name__ == "__main__":
    cli()                                        # cli ko call krr rahe hain