from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.contrib import messages
from django.utils.text import slugify
from django.template.defaultfilters import slugify 

from user.models import *
from .models import Article, Tag, Category, Comment , Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
# Create your views here.
from .forms import FormText, AddArticle
from django.db.models import Q

def home(request):
    articles = Article.objects.order_by('-created_at')
    tags  = Tag.objects.order_by('-created_at')
    context = {
        "articles": articles,
        'tags': tags
    }
    return render(request, 'home.html', context)

def articles(request):
    articles = Article.objects.order_by('-created_at')
    page = request.GET.get('page', 1)
    # number of articles per page
    paginator = Paginator(articles, 5)

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        articles = paginator.page(1)
        return redirect('articles')
    except EmptyPage:
        # If page is out of range deliver last page of results
        articles = paginator.page(paginator.num_pages)

    tags  = Tag.objects.order_by('-created_at')
    context = {
        "articles": articles,
        'tags': tags,
        'paginator': paginator,
    }
    return render(request, 'articles.html', context)
# page des categories

def category_articles(request, slug):
    category = Category.objects.get(slug=slug)
    articles = category.categorie_aticles.all()
    tags  = Tag.objects.order_by('-created_at')[:5]
    page = request.GET.get('page', 1)
    # number of articles per page
    paginator = Paginator(articles, 5)
    articles_all = Article.objects.order_by('-created_at')[:5]

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        articles = paginator.page(1)
        return redirect('articles')
    except EmptyPage:
        # If page is out of range deliver last page of results
        articles = paginator.page(paginator.num_pages)
    context = {
        "articles": articles,
        "tags":  tags,
        'paginator': paginator,
        'articles_all': articles_all,

    }
    return render(request, 'category_articles.html', context)

# page en fonction des tag
def tag_articles(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    articles = tag.tag_articles.all()
    tags  = Tag.objects.order_by('-created_at')[:5]
    page = request.GET.get('page', 1)
    # number of articles per page
    paginator = Paginator(articles, 5)
    articles_all = Article.objects.order_by('-created_at')[:5]

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        articles = paginator.page(1)
        return redirect('articles')
    except EmptyPage:
        # If page is out of range deliver last page of results
        articles = paginator.page(paginator.num_pages)
    context = {
        "articles": articles,
        "tags":  tags,
        'paginator': paginator,
        'articles_all': articles_all,

    }
    return render(request, 'tag_articles.html', context)


def details_articles(request, slug):
    article = get_object_or_404(Article, slug=slug)
    tags  = Tag.objects.order_by('-created_at')[:5]
    category = Category.objects.get(id=article.category.id)
    related_articles = category.categorie_aticles.all().exclude(id=article.id)[:3]
    form = FormText()
    liked = request.user in article.likes.all()
    if request.method == 'POST' and  request.user.is_authenticated:
      form = FormText(request.POST)
      if form.is_valid():
          Comment.objects.create(
              user=request.user,
                article=article,
                text=form.cleaned_data.get('text')
          )  
          return redirect('details_articles', slug=slug)  
    context = {
        "article": article,
        "tags":  tags,
        'related_articles': related_articles,
        'form': form,
        'liked': liked
        
    }
    return render(request, 'details_articles.html', context)

@login_required(login_url='login')
def add_reply(request, article_id, comment_id):
    articles = get_object_or_404(Article, id=article_id)
    if request.method == "POST":
        form = FormText(request.POST)
        if form.is_valid():
            comment = get_object_or_404(Comment, id=comment_id)
            Response.objects.create(
                user=request.user,
                comment=comment,
                text=form.cleaned_data.get('text')
            )
    return redirect('details_articles', slug=articles.slug)

@login_required(login_url='login')
def likes(request, pk):
    context = {}
    article = get_object_or_404(Article, pk=pk)

    # Vérifiez si l'utilisateur est l'auteur de l'article
    if request.user == article.user:
        context['error'] = "You cannot like your own article."
        return JsonResponse(context, safe=False, status=400)

    if request.user in article.likes.all():
        article.likes.remove(request.user)
        context['liked'] = False
        context['like_count'] = article.likes.all().count()
    else:
        article.likes.add(request.user)
        context['liked'] = True
        context['like_count'] = article.likes.all().count()

    return JsonResponse(context, safe=False)


def search(request):
    key_search = request.GET.get('search', None)
    recent = Article.objects.order_by('-created_at')
    tags  = Tag.objects.order_by('-created_at')[:5]

    if key_search:
        articles = Article.objects.filter(
            Q(title__icontains=key_search) | Q(description__icontains=key_search) |Q(user__username__icontains=key_search) |
            Q(tags__title__icontains=key_search) | Q(category__title__icontains=key_search)
        ).distinct()
        context = {
            "recent_articles": recent,
            "tags":  tags,
            "articles": articles,
            "key_search": key_search
        
        }

        return render(request, 'search.html', context)
    else:
       
        return redirect('home')
    

@login_required(login_url='login')    

def my_articles(request):
    queryset = request.user.user_articles.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 6)

    try:
        articles = paginator.page(page)
    except EmptyPage:
        articles = paginator.page(1)
    except PageNotAnInteger:
        articles = paginator.page(1)
   

    context = {
        "articles": articles,
        "paginator": paginator
    }
    
    return render(request, 'myarticle.html', context)

@login_required(login_url='login')
def add_article(request):
    if request.method == 'POST':
        form = AddArticle(request.POST, request.FILES)
        if form.is_valid():
            tags = request.POST.get('tags', '').split(',')
            user = get_object_or_404(User, pk=request.user.pk)
            category = get_object_or_404(Category, pk=request.POST['category'])

            article = form.save(commit=False)
            article.user = user
            article.category = category
            article.save()  # Enregistrez l'article en base de données d'abord

            for tag_title in tags:
                tag_title = tag_title.strip()
                if tag_title:
                    tag, created = Tag.objects.get_or_create(
                        title=tag_title, slug=slugify(tag_title)
                    )
                    article.tags.add(tag)

            messages.success(request, 'Article added successfully')
            return redirect('my_articles')
    else:
        form = AddArticle()

    context = {
        "form": form
    }
    return render(request, 'article_add.html', context)


  

@login_required(login_url='login')    
def my_articles(request):
    queryset = request.user.user_articles.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 6)
    delete = request.GET.get('delete', None)

    if delete:
        article = get_object_or_404(Article, pk=delete)
        if request.user.pk != article.user.pk:
            return redirect('home')
        article.delete()
        messages.success(request, 'Article deleted successfully')
        return redirect('my_articles')

    try:
        articles = paginator.page(page)
    except EmptyPage:
        articles = paginator.page(1)
    except PageNotAnInteger:
        articles = paginator.page(1)
   

    context = {
        "articles": articles,
        "paginator": paginator
    }
    
    return render(request, 'myarticle.html', context)

@login_required(login_url='login')
def update_article(request, slug):
    articles = Article.objects.filter(slug=slug)
    if articles.count() == 0:
        return redirect('home')  # Aucun article trouvé avec ce slug, rediriger vers la page d'accueil
    elif articles.count() == 1:
        article = articles.first()  # Un seul article trouvé avec ce slug
    else:
        article = articles.first()

    form = AddArticle(instance=article)

    if request.method == 'POST':
        form = AddArticle(request.POST, request.FILES, instance=article)

        if form.is_valid():
            if request.user.pk != article.user.pk:
                return redirect('home')

            # Assurez-vous que le slug est unique avant de sauvegarder l'article
            new_slug = slugify(form.cleaned_data['title'])
            if Article.objects.filter(slug=new_slug).exclude(pk=article.pk).exists():
                new_slug = f"{new_slug}-{article.pk}"  # Ajoutez l'ID de l'article pour le rendre unique

            article.slug = new_slug  # Mette à jour le slug
            article.save()

            # Supprimez d'abord les anciens tags de l'article
            article.tags.clear()

            tags = request.POST['tags'].split(',')
            user = get_object_or_404(User, pk=request.user.pk)
            category = get_object_or_404(Category, pk=request.POST['category'])
            article = form.save(commit=False)
            article.user = user
            article.category = category
            article.save()

            for tag in tags:
                tag = tag.strip()
                tag_exists = Tag.objects.filter(title__iexact=tag)
                
                if tag_exists.exists():
                    t = tag_exists.first()
                    article.tags.add(t)
                elif tag != '':
                    # Generate a unique slug for the new tag
                    new_tag_slug = slugify(tag)
                    counter = 1
                    while Tag.objects.filter(slug=new_tag_slug).exists():
                        new_tag_slug = slugify(f"{tag}-{counter}")
                        counter += 1
                    
                    newTag = Tag.objects.create(title=tag, slug=new_tag_slug)
                    article.tags.add(newTag)

            messages.success(request, 'Article updated successfully')
            return redirect('my_articles')

        else:
            print(form.errors)
    
    context = {
        "form": form,
        "article": article
    }
    return render(request, 'update.html', context)
