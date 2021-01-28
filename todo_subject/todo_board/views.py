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

class Todo_board_update(generic.UpdateView):
    model = TodoList
    fields = ('title', 'content', 'end_date')
    template_name = 'todo_board/todo_board_update.html'
    # success_url 은 업데이트 성공 시 이동하는 url
    success_url = '/board/'

    # save 기능
    def form_valid(self, form):
        form.save()
        return render(self.request, 'todo_board/todo_board_success.html', {"message":"일정을 업데이트 하였습니다."})

    # form 데이터 받아오는 기능
    def get(self, request, *args, **kwargs):
        # 오브젝트를 받아와서 폼 클래스를 받아온 후 이것을 return 해줘야 한다.
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

class Todo_board_delete(generic.DeleteView):
    model = TodoList
    success_url = '/board/'
    context_object_name = 'todo_list'
