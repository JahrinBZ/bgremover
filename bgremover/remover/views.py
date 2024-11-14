from django.shortcuts import render
from django.core.files.storage import default_storage
from django.conf import settings
import os
from rembg import remove
from PIL import Image

def home(request):
    ogimage = None
    bgrimage = None

    if request.method == 'POST':
        image = request.FILES.get('image-upload')
        clear_folder(os.path.normpath(os.path.join(settings.MEDIA_ROOT, 'ogimages')))
        clear_folder(os.path.normpath(os.path.join(settings.MEDIA_ROOT, 'bgrimages')))
        if image:
            # Define the filesystem path for the original image
            ogimage_path = os.path.normpath(os.path.join(settings.MEDIA_ROOT, 'ogimages', image.name))
            os.makedirs(os.path.dirname(ogimage_path), exist_ok=True)
            
            # Save the original image
            file_path = default_storage.save(ogimage_path, image)
            ogimage_path = os.path.normpath(os.path.join(settings.MEDIA_ROOT, 'ogimages', image.name)).replace("\\", "/")
            og_url=os.path.normpath(os.path.join(settings.MEDIA_URL, 'ogimages', image.name)).replace("\\", "/")
            
            # Open the saved image using the correct filesystem path
            with Image.open(ogimage_path) as input_image:
                # Remove the background
                output_image = remove(input_image)
                
                # Define the path for the processed image
                if output_image.mode == 'RGBA':
                    output_image = output_image.convert('RGB')
                
                # Define the path for the processed image
                bgrimage_path = os.path.normpath(os.path.join(settings.MEDIA_ROOT, 'bgrimages', image.name))
                os.makedirs(os.path.dirname(bgrimage_path), exist_ok=True)

                # Save the processed image as a JPEG
                output_image.save(bgrimage_path, format="JPEG")
                bgrimage_url = os.path.normpath(os.path.join(settings.MEDIA_URL, 'bgrimages', image.name)).replace("\\", "/")

            ogimage = og_url
            bgrimage = bgrimage_url
            

    data = {'ogimage': ogimage, 'bgrimage': bgrimage}
    print(data)
    return render(request, "Hello.html", data)


def clear_folder(folder_path):
    """Remove all files from the specified folder."""
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")