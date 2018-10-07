from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Schemes, Category, Products
from django.http import Http404
from harbacore_home import UtitlityFunctions

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def schemes_list(request, scheme_id=1):
    print ("in schemes")
    try :
        schemes_list = Schemes.objects.filter(is_active=True)
        selected_scheme = Schemes.objects.get(pk = scheme_id)
        tc = UtitlityFunctions.seperateStringOnBasisOfHtmlTags(
                                                        selected_scheme.terms_and_conditions,
                                                        ["<ul>","</ul>","<li>", "</li>"])
        terms_and_conditions = []
        for t_c in tc:
            if len(t_c)>0 and t_c!='':
                terms_and_conditions.append(t_c)

        context = {
            'schemes_list' : schemes_list,
            'selected_scheme': selected_scheme,
            'terms_and_conditions': terms_and_conditions
        }
        # print("schemes list",schemes_list)
        # print("selected scheme ", selected_scheme)
        # print("terms ---> ",terms_and_conditions)
        return render(request=request, template_name='home_module/schemes_list.html', context=context)
    except Exception as e:
        print ("Exception as ", e)
        return render(request=request, template_name='home_module/page_404.html')


def product_list(request, category_id=2):
    print("in products")
    categories = Category.objects.filter(is_active=True)
    print ("categories ", categories)
    #can use _set.all() function too for a particular category in the html

    category_name = Category.objects.get(pk=category_id).category_name
    products = Products.objects.filter(product_category__id=category_id)

    processed_products_data =[]
    for product in products:
        temp = {}
        temp['product'] = product
        temp['final_price'] = product.product_mrp - 0.01*product.product_discount*product.product_mrp;
        processed_products_data.append(temp)

    print ("processed ", processed_products_data)
    context = {
        'categories': categories,
        'data'  : processed_products_data,
        'category_name' : category_name
    }

    return render(request=request, template_name='home_module/category_list.html', context=context)