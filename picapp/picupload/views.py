from django.shortcuts import render, redirect
from .models import Files
from django.contrib import messages
from next_prev import next_in_order, prev_in_order

# Home page
def home(request):
    if request.method == 'POST':

        # list of files uploaded
        files = request.FILES.getlist('files')

        # if no files uploaded then it will produce an error
        if len(files) < 1:
            messages.error(request, 'No files selected')
            return render(request, 'home.html')

        # if files uploaded then append to database
        else:
            for file in files:
                new_file = Files (
                    file = file
                )
                new_file.save()
            messages.success(request ,'Your file has been succesfully uploaded')

            # filename extracted from file field using first id from database
            file_id = Files.objects.first().id
            return  redirect('imagetag', id= file_id)
    else:
        return render(request, 'home.html' )
        

# Image tag page
def imagetag(request , id):
    
    allimages = Files.objects.get(id=id)
    if request.method == 'POST':
        
        # previous button clicked
        if request.POST.get('prev'):
            print('blaaa' + request.POST.get('prev'))
            prev_image = prev_in_order(allimages)
            print(prev_image.id)
            # if no previous image
            if prev_image == None:
                messages.error(request, 'No more images')
                return redirect('imagetag', id=id+1)
                # Note: 'id' is incremented because of no more images i.e. id = first.id + 1
            
            # filename extracted from file field
            filename_prev = prev_image.file.name
            filename_prev = filename_prev.split('/')[-1]

            return render(request,'imagetag.html', {'prev': prev_image ,'fname_prev': filename_prev})
            # Note: 'prev' is used to display previous image in template

        # next button clicked
        if request.POST.get('next'):
            print(request.POST.get('next'))
            next_image = next_in_order(allimages)

            # no more images left or no images in database
            if next_image == None:
                messages.error(request, 'No more images')
                return redirect('imagetag', id=id-1)
                # Note: 'id' is decremented because of no more images i.e. id = last.id - 1

            # filename extracted from file field
            filename_nxt = next_image.file.name
            filename_nxt = filename_nxt.split('/')[-1]
            return render(request,'imagetag.html',{'next': next_image ,'fname_nxt': filename_nxt})
            # Note: 'fname_nxt' is used in html to display filename 

        # file name updated 
        if request.POST.get('upd_name'):
            new_fname = request.POST.get('upd_name')
            allimages.file.name = new_fname
            allimages.save()
            messages.success(request, 'File name updated')
            return render(request, 'imagetag.html' )

    return render(request, 'imagetag.html')
    
