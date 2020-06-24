from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View

from .models import Product, Review
from .forms import ReviewForm


def product_list_view(request):
    template = 'app/product_list.html'
    products = Product.objects.all()

    context = {
        'product_list': products,
    }

    return render(request, template, context)


class ProductView(View):
    form_class = ReviewForm
    template_name = 'app/product_detail.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        pk = kwargs.get('pk')
        product = get_object_or_404(Product, id=pk)
        reviews = Review.objects.filter(product_id=product.id)

        context = {
            'product': product,
            'reviews': reviews,
        }
        reviewed_products = request.session.get('reviewed_products')

        if reviewed_products is None or pk not in reviewed_products:
            context.update({'form': form, })
        else:
            context.update({'is_review_exist': True, })

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        product = get_object_or_404(Product, id=pk)
        reviewed_products = request.session.get('reviewed_products')
        if reviewed_products is None:
            reviewed_products = []

        if pk not in reviewed_products:
            reviewed_products.append(pk)
            review_text = request.POST.get('text')
            Review.objects.create(text=review_text, product=product)

        request.session['reviewed_products'] = reviewed_products

        return HttpResponseRedirect(request.path)
