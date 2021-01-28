import os

from django.shortcuts import reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, FormView

from .forms import ImageUploadForm, ImageResizeForm
from .models import Image
from .utils import resize_image


class ImageListView(ListView):
    model = Image
    context_object_name = 'images'
    template_name = 'index.html'


class ImageCreateView(CreateView):
    form_class = ImageUploadForm
    template_name = 'images/upload.html'

    def get_success_url(self):
        return reverse('update', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        image = form.save()
        name = os.path.basename(image.original_image.name)
        image.resized_image.save(name, image.original_image)
        return super().form_valid(form)


class ImageResizeView(FormView):
    form_class = ImageResizeForm
    template_name = 'images/update.html'
    success_url = reverse_lazy('update')

    def get_success_url(self):
        return reverse('update', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image'] = get_object_or_404(Image, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        source = get_object_or_404(Image, pk=self.kwargs['pk'])
        width = form.cleaned_data['width']
        height = form.cleaned_data['height']
        resize_image(source, width, height)
        return super().form_valid(form)
