from django.shortcuts import render, redirect
from django.views import generic
from .models import TodoList
from .forms import TodoForm
from datetime import datetime

# board view
class Todo_board(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        # todo_main에 있는 템플릿 폴더에서 해당 html을 찾으시오.
        template_name = 'todo_board/todo_board_list.html'
        # 기한이 없는 일정, 마감 안된 일정 --> 모든 객체를 가져옴.
        todo_list_no_endDate = TodoList.objects.all().filter(end_date__isnull=True, is_complete=0).order_by('priority')
        #기한 있고, 마감이 안된 애들
        todo_list_endDate_non_complete = TodoList.objects.all().filter(end_date__isnull=False, is_complete=0).order_by('priority')
        #마김이 된 애들
        todo_list_endDate_complete = TodoList.objects.all().filter(is_complete=1).order_by('end_date')
        today = datetime.now()
        # 마감이 가까운 일정
        close_end_day = []
        # 마감이 지난 일정
        over_end_day = []
        for i in todo_list_endDate_non_complete:
            e_day = str(i.end_date).split("-")
            end_day = datetime(int(e_day[0]), int(e_day[1]), int(e_day[2]))
            if (end_day - today).days < -1: over_end_day.append(i.title)
            if (end_day - today).days >= -1 and (end_day - today).days < 3: close_end_day.append(i.title)
        return render(request, template_name, {"todo_list_endDate_non_complete": todo_list_endDate_non_complete, "todo_list_endDate_complete": todo_list_endDate_complete, "todo_list_no_endDate": todo_list_no_endDate, 'close_end_day': close_end_day, 'over_end_day':over_end_day})


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
