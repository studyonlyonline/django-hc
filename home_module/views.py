from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Schemes, Category, Products
from django.http import Http404
from harbacore_home import UtitlityFunctions
from django.views import View, generic
import json

def index(request):
    if request.session.get('cart') is not None:
        print ("Cart in index page" ,request.session.get('cart'))
    else:
        print("cart is empty in index page")
    return HttpResponse("Hello, world. You're at the polls index.")

#get the user
def getCurrentUser(request):
    if request.user.is_authenticated:
        return request.user

class SchemesListView(View):
    scheme_id = 1

    def get(self, request,*args, **kwargs):
        if 'scheme_id' in self.kwargs and self.kwargs['scheme_id'] is not None:
            self.scheme_id = self.kwargs['scheme_id']

        # print ("kwargs ", kwargs)
        # print ("self.kwargs ", self.kwargs)
        # print ("in schemes")
        try :
            schemes_list = Schemes.objects.filter(is_active=True)
            selected_scheme = Schemes.objects.get(pk = self.scheme_id)
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


class ProductListView(View):
    #default category
    category_id = 2
    def get(self,request,*args, **kwargs):
        if 'category_id' in self.kwargs and self.kwargs['category_id'] is not None:
            self.category_id = self.kwargs['category_id']

        print ("kwargs ", kwargs)
        print ("self.kwargs ", self.kwargs)
        print("in products get")

        categories = Category.objects.filter(is_active=True)
        print ("categories ", categories)
        #can use _set.all() function too for a particular category in the html

        category_name = Category.objects.get(pk=self.category_id).category_name
        products = Products.objects.filter(product_category__id=self.category_id)

        processed_products_data =[]
        for product in products:
            temp = {}
            temp['product'] = product
            temp['final_price'] = product.product_mrp - 0.01*product.product_discount*product.product_mrp;
            processed_products_data.append(temp)

        # print ("processed ", processed_products_data)
        context = {
            'categories': categories,
            'data'  : processed_products_data,
            'category_name' : category_name,
        }

        return render(request=request, template_name='home_module/category_list.html', context=context)

class AddToCartSessionView(View):

    def get(self, request, *args, **kwargs):
        print("AddToCartSessionView GET method")
        print ("session object ", request.session)
        print ("GET  params", request.GET)
        item_id = request.GET.get('item_id')
        item_quantity = request.GET.get('quantity')
        print ("item_id ->", item_id, "item_quanitty -> ", item_quantity)

        cart = request.session.get('cart', {})
        print("Cuurent cart before adding ", cart)

        if cart.get(item_id) is not None:
            messages.add_message(request=request, message="Item already present in Cart", level=messages.INFO)
        else:
            try:
                product = Products.objects.get(pk=int(item_id))
                updateData = {
                    item_id: int(item_quantity)
                }
                request.session = UtitlityFunctions.updateSessionObject(request, 'cart', updateData)
                request.session.modified = True
                print("After cart after adding ", request.session.get('cart'))
                # add message and display on page
                messages.add_message(request=request, message="Added to cart", level=messages.SUCCESS)

            except Products.DoesNotExist:
                messages.add_message(request=request, message="Product Does not exist", level=messages.SUCCESS)

        print ("Added to Cart")
        return redirect(reverse_lazy('home_module:cart'))


    def post(self, request, *args, **kwargs):
        print("Addtocart POST called")
        print("POST Cart object ", request.session.get('cart', {}))
        print ("session object ", request.session)
        print ("POST  params", request.POST)
        item_id = request.POST.get('item_id')
        item_quantity = request.POST.get('item_quantity')
        print("item_id ->", item_id, "item_quanitty -> ", item_quantity)
        print ("type of item_id ", type(item_id))

        try:
            product = Products.objects.get(pk=int(item_id))
            max_quantity = product.product_quantity
            print("max quantity ", max_quantity)
            if max_quantity < int(item_quantity):
                item_quantity = int(max_quantity)
                messages.add_message(request=request, message="Max quantity is " + str(max_quantity), level=messages.SUCCESS)
            update_data = {
                item_id: int(item_quantity)
            }
            request.session = UtitlityFunctions.updateSessionObject(request, 'cart', update_data)
            print("Cart dictionary after utilityFunction called ", request.session.get('cart', {}))
            return redirect(reverse_lazy('home_module:cart'))

        except Exception as e:
            print ("redirect to 404", e)
            redirect(render(request=request, template_name='home_module/page_404.html'))

class CartView(View):

    def get(self, request, *args, **kwargs):

        try:
            #getting cart session
            print("CartView")
            cart = request.session.get('cart', {})
            print ("Cart in Cart View" , cart)
            is_cart_empty = True
            total_amount = 0
            data = []
            if len(cart) > 0:
                is_cart_empty = False
                for item_id, item_quantity in cart.items():
                    print ("type is ", type(item_id))
                    item_id = int(item_id)
                    item_quantity = int(item_quantity)
                    # print ("cart item_id "+str(item_id)+" item_quantity "+str(item_quantity))
                    product = get_object_or_404(Products, pk=item_id)
                    #adding item to data list to be finally shown to cart

                    temp = {}
                    temp['product_name'] = product.product_name
                    temp['product_quantity'] = item_quantity
                    temp['product_id'] = item_id
                    temp['product_final_price'] = product.product_mrp - 0.01*product.product_discount*product.product_mrp;
                    temp['product_mrp'] = product.product_mrp
                    temp['product_discount'] = product.product_discount
                    temp['final_quantity_amount'] = item_quantity * temp['product_final_price']
                    total_amount = total_amount +  temp['final_quantity_amount'];
                    data.append(temp)

            context = {
                'data': data,
                'is_cart_empty': is_cart_empty,
                'total_amount' : total_amount
            }
            print ("data ",data)
            return render(request=request, template_name='home_module/cart.html', context=context)

        except Exception as e:
            print ("Exception in cart ", e)
            return render(request=request, template_name='home_module/page_404.html')

class UpdateCartQuantity(View):

    def get(self, request, *args, **kwargs):
        print ("UpdateCartQuantityView Cart object ", request.session.get('cart',{}))
        request.session = UtitlityFunctions.updateSessionObject(request, 'cart', {kwargs['id']:kwargs['quantity']})
        print("Cart dictionary after utilityFunction called ", request.session.get('cart', {}))
        return HttpResponse("yes")

class TestListView(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):
        context = {
            'data' : self.kwargs['name']
        }
        return render(request=request, template_name="home_module/test.html", context=context)

class SubmitOrderView(LoginRequiredMixin,View):

    def get(self,request):
        print ("inside SubmitOrder view")

        return HttpResponse("Order submitted")




















