from django.shortcuts import render,redirect

from django.views import View

from .forms import RegisterForm , LoginForm , ImageForm

from django.contrib.auth import authenticate,login,logout
from .models import CategoryModel,ImageModel
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from .dl_model.model import classify_image

from django.http import QueryDict


# Create your views here.

def signout_view(request):
    logout(request)
    
    return redirect('home')


class home_view(View):

    def get(self , request):
        if request.user.is_authenticated:
            return redirect('addimage')

        forms = LoginForm()
        context = {'forms':forms}
        print(request.user)
        print(type(request.user))

        

        print("context is ")
        print(context)
        return render(request , 'home.html' , context)

    def post(self , request):

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username , password = password)

        if user is not None:
            login(request , user)
            
            return redirect('gallery')

        return redirect('home')


class register_view(View):
    def get(self , request):

        if request.user.is_authenticated:
            return redirect('gallery')

        forms = RegisterForm()
        context = {'forms':forms}

        return render(request , 'register.html' , context)

    def post(self , request):

        forms = RegisterForm(request.POST)
        if forms.is_valid():
            forms.save()

            return redirect('home')

        context = {'forms':forms}
        return render(request , 'register.html' , context)

class gallery_view(View):
    def get(self , request):
        category = CategoryModel.objects.all()
        Images = ImageModel.objects.all()

        context = {'category':category , 'Images':Images}
        return render(request , 'gallery.html',context)

    def post(self , request):
        return render(request , 'gallery.html')
        # return redirect('gallery')

class Cat_view(View):
    def get(self , request ,id):
        Images = ImageModel.objects.filter(cat = id)
        category = CategoryModel.objects.all()

        context = {'category':category , 'Images':Images}
        return render(request , 'gallery.html',context)



class myupload_view(View) :
    def get(self ,request):
        Images =ImageModel.objects.filter(uploaded_by = request.user)
        context = {'Images':Images}
        return render(request , 'myupload.html',context)   



class addimage_view(View):
    def get(self , request):
        forms = ImageForm()
        context = {'forms':forms}
        
        return render(request , 'addimage.html',context)

    def post(self , request):
        img = request.FILES['image']
        img.seek(0)
         #  convert the file to bytes
        image = img.read()
        result = classify_image(image)
        #Select the top three predictions according to their probabilities
        top1 = '1. Species: %s, Status: %s, Probability: %.4f'%(result[0][0], result[0][1], result[0][2])
        top2 = '2. Species: %s, Status: %s, Probability: %.4f'%(result[1][0], result[1][1], result[1][2])
        top3 = '3. Species: %s, Status: %s, Probability: %.4f'%(result[2][0], result[2][1], result[2][2])

        predictions = [ { 'pred':top1 }, { 'pred':top2 }, { 'pred':top3 } ]
        print(predictions)

        img.seek(0)
        context = { 'predictions':predictions }

        q = QueryDict()
        d={}
        
        catmap={"Apple":"4","Blueberry":"5","Cherry":"6","Corn":"7","Grape":"8","Orange":"9","Peach":"10","Pepper,":"11","Potato":"12","Raspberry":"13","Soybean":"14","Squash":"15","Strawberry":"16","Tomato":"17","Corn_(maize)":'18',"Cherry_(including_sour)":"19","Pepper,_bell":"20"}
        d['csrfmiddlewaretoken'] = request.POST['csrfmiddlewaretoken']
        d['title'] = result[0][0] +"  "+ result[0][1] 
        
        d['cat'] = catmap[result[0][0]]
        # d['cat'] = request.POST['cat']
        d['desc'] = f'{top1}'
  
        q = QueryDict('', mutable=True)
        q.update(d)
        forms = ImageForm(q , request.FILES)
        

        if forms.errors:
            print(forms.errors)
        if forms.is_valid():
            print(request.POST)
            print(type(request.POST))

            task = forms.save(commit=False)
            
            task.uploaded_by = request.user
            task.save()

            fs = FileSystemStorage()
            filename = fs.save(request.FILES['image'].name, request.FILES['image'])
            uploaded_file_url = fs.url(filename)
            context['url'] = uploaded_file_url
            # return redirect('gallery')
            return render(request, 'predict.html', context)
        return render(request , 'addimage.html')
            

#    create view for single view img 
def view_image(request,image_id):
        print(type(image_id))
        image = ImageModel.objects.get(id=image_id)
        print('inside view')
        print(image)

        context = {'image': image}
        print(context)
        print(request)
        return render(request, 'image.html', context) 


def about_view(request):
    return render(request , 'about.html')
