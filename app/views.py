from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .models import Product, Review
from .forms import ReviewForm


def product_list_view(request):
    template = 'app/product_list.html'
    products = Product.objects.all()

    context = {
        'product_list': products,
    }

    return render(request, template, context)


def product_view(request, pk):
    template = 'app/product_detail.html'
    product = get_object_or_404(Product, id=pk)

    form = ReviewForm
    if request.method == 'POST':
        reviewed_products = request.session.get('reviewed_products')
        if reviewed_products is None:
            reviewed_products = []

        if pk not in reviewed_products:
            reviewed_products.append(pk)
            review_text = request.POST.get('text')
            Review.objects.create(text=review_text, product=product)

        request.session['reviewed_products'] = reviewed_products

    reviews = Review.objects.filter(product_id=product.id)

    context = {
        'product': product,
        'reviews': reviews,
    }

    reviewed_products = request.session.get('reviewed_products')

    if reviewed_products is None or pk not in reviewed_products:
        context.update({'form': form,})
    else:
        context.update({'is_review_exist': True,})

    return render(request, template, context)
