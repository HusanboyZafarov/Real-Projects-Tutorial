import json
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Count
from django.views.generic import ListView, UpdateView
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from account.models import User
from django.template.defaultfilters import slugify
from .models import Work, Banner
from .forms import ContactForm, WorkForm


def likes_views(request):
    d = request.GET['data']
    data = json.loads(d)
    work_id = data['id']
    work = Work.objects.select_related('author').get(id=work_id)
    request.session.modified = True
    context = {
        'status': 400
    }
    post_id = work.id
    try:
        liked_posts = request.session["like_list"]
    except:
        liked_posts = request.session["like_list"] = []

    if post_id not in liked_posts:
        liked_posts.extend([post_id])
        work.likes += 1
        work.author.total_likes += 1
        work.author.save()
        work.save()
        context['status'] = 10
    else:
        liked_posts.remove(post_id)
        work.likes -= 1
        work.author.total_likes -= 1
        work.author.save()
        work.save()
        context['status'] = 20

    return JsonResponse(context)


# views count increase
def get_view_list(request, obj):
    request.session.modified = True
    post_id = obj.id
    try:
        viewed_posts = request.session["view_list"]
    except:
        viewed_posts = request.session["view_list"] = []

    if post_id not in viewed_posts:
        viewed_posts.extend([post_id])
        obj.views_count += 1
        obj.save()
    else:
        print(viewed_posts)


class ProjectList(ListView):
    queryset = Work.objects.select_related('author')
    paginate_by = 12
    context_object_name = 'works'
    template_name = 'work.html'


class MyProjectList(ListView):
    queryset = Work.objects.select_related('author')
    paginate_by = 12
    context_object_name = 'works'
    template_name = 'work.html'

    def get_queryset(self):
        queryset = super(MyProjectList, self).get_queryset()
        queryset = queryset.filter(author__username=self.kwargs['username'])
        return queryset


def home_view(request):
    top_works = Work.objects.select_related('author').alias(nlikes=Count(
        'likes')).order_by('-nlikes', '-views_count', '-created_at')[:6]
    top_students = User.objects.order_by(
        '-total_likes', '-total_works', '-created_at')[:6]
    students_ratings = User.objects.order_by(
        '-total_likes', '-total_works', '-created_at')[:10]
    banners = Banner.objects.order_by('-id')
    context = {
        'top_works': top_works,
        'top_students': top_students,
        'student_ratings': students_ratings,
        'banners': banners
    }
    return render(request, 'index.html', context)


def create_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Muvaffaqiyatli jo'natildi !")
            return redirect('/')
        return redirect('/')
    else:
        messages.info(request, "Muvaffaqiyatli jo'natildi !")
        return redirect('/')


@login_required
def create_project(request):
    if request.method == 'POST':
        work_form = WorkForm(request.POST, request.FILES)
        if work_form.is_valid():
            print('ok')
            f = work_form.save(commit=False)
            f.author = request.user
            f.slug = slugify(f.title)
            f.save()
            request.user.total_works += 1
            request.user.save()
            messages.info(request, "Ishingiz muvaffaqiyatli qo'shildi !")
            return redirect(f'/projects/{request.user.username}')

    return render(request, 'create-work.html')


def project_detail(request, slug):
    work = Work.objects.select_related('author').get(slug=slug)
    autor_works = Work.objects.select_related('author').filter(
        author=work.author).exclude(slug=slug)[:2]
    get_view_list(request, work)
    return render(request, 'detail.html', {'work': work, 'author_works': autor_works})


@login_required
def project_update(request, slug):
    work = Work.objects.select_related('author').get(slug=slug)
    if request.method == 'POST':
        if work.author == request.user:
            form = WorkForm(request.POST, request.FILES, instance=work)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.INFO,
                                     'Ishingiz muvaffaqiyatli tahrirlandi !')
                return redirect(f'/projects/{request.user.username}')
        else:
            messages.add_message(request, messages.INFO,
                                 'Siz ushbu ishning egasi emassiz !')
            return redirect(f'/projects/{request.user.username}')

    return render(request, 'create-work.html', {'object': work})


@login_required
def project_delete(request, slug):
    obj = Work.objects.get(slug=slug)
    if request.method == 'POST':
        if request.user == obj.author:
            obj.author.total_works -= 1
            obj.author.save()
            obj.delete()
            messages.add_message(request, messages.INFO,
                                 'Ish o\'chirib tashlandi !')
            return redirect('/')
        else:
            messages.add_message(request, messages.INFO,
                                 'Siz ushbu ishning egasi emassiz !')
            return redirect('/')
    return render(request, 'delete-confirm.html', {'object': obj})


def help(request):
    return render(request, "help.html")
