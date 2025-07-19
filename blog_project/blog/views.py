from django.shortcuts import render,redirect,get_object_or_404
from .models import Post
from .forms import PostForm
from .monitoring import log_to_cloudwatch
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                logger.info('AWS_STORAGE_BUCKET_NAME:' + settings.AWS_STORAGE_BUCKET_NAME)
                logger.info('REGION:' + settings.AWS_S3_REGION_NAME)
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                log_message = f"New post created: {post.title}"
                log_to_cloudwatch(log_message, "DjangoBlogLogs", "PostCreation")
                logger.info(log_message)
                return redirect('post_detail', pk=post.pk)
            except Exception as e:
                error_message = f"Error creating post: {str(e)}"
                log_to_cloudwatch(error_message, "DjangoBlogLogs", "PostCreationError")
                logger.error(error_message)
                form.add_error(None, "An error occurred while creating the post. Please try again.")
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    posts = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': posts})

