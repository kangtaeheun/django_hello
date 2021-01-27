from django.shortcuts import render, redirect
from django.views import generic
from .models import TodoList
from .forms import TodoForm

# board view
class Todo_board(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        # todo_main에 있는 템플릿 폴더에서 해당 html을 찾으시오.
        template_name = 'todo_board/todo_board_list.html'
        # 모든 객체를 가져옴.
        todo_list = TodoList.objects.all()
        # 그 결과값을 {'todo_list':todo_list}에 담아서 template로 넘겨줌.
        return render(request, template_name, {'todo_list': todo_list})

# generic.DetailView를 이용하면 굉장히 편하게 상세보기 페이지를 만들 수 있음.
class Todo_board_detail(generic.DetailView):
    model = TodoList
    template_name = 'todo_board/todo_board_detail.html'
    context_object_name = 'todo_list' # context_object_name은 해당 object의 이름을 설정. template에서 저 이름을 가지고 접

def check_post(request):
    template_name = 'todo_board/todo_board_success.html'
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            message = "일정을 추가하였습니다."
            todo.todo_save()
            return render(request, template_name, {"message": message})
    else:
        template_name = 'todo_board/todo_board_insert.html'
        form = TodoForm
        return render(request, template_name, {'form' : form})
