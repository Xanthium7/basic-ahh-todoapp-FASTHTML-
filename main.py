from fasthtml.common import *


def render(todo):
    tid = f"todo-{todo.id}"
    toggle = A('Toggle',  hx_get=f"/toggle/{todo.id}", target_id=tid)
    delete = A('Delete',  hx_get=f"/delete/{todo.id}", target_id=tid)
    return Li(todo.title + (' ✅' if todo.done else " ✖️"), toggle, (Span(" "))+delete,  id=tid)


app, rt, todos, Todo = fast_app(
    'todos.db', live=True, id=int, title=str, done=bool, pk='id', render=render)


@rt('/')
def post(todo: Todo):
    return todos.insert(todo)


@rt('/')
def get():
    frm = Form(Group(Input(placeholder="Add new Todo", name='title'),
               Button("Add")), hx_post="/", target_id='todo-list', hx_swap='beforeend')
    return Titled('Todo App',
                  Div(P('Hello Akshhay!!!'),
                      Card(
                      Ul(*todos(), id='todo-list'),
                      header=frm
                  ),
                  ))


@rt('/toggle/{tid}')
def get(tid: int):
    todo = todos[tid]
    todo.done = not todo.done
    todos.update(todo)
    return todo


@rt('/delete/{tid}')
def get(tid: int):
    todo = todos[tid]
    todos.delete(todo)
    return todo


serve()
