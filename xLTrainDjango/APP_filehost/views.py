import environ
from django.shortcuts import render, redirect
from transliterate import translit
from APP_home.models import User
from params_and_funcs import reCAPTCHA_validation, log
from .models import Upload, UploadedFile

env = environ.Env()


def DeleteUpload(request, pk=None):
    if pk is None:
        return render(request, 'NotFound.html')
    upload_ = Upload.objects.get(id=pk)

    if upload_.username.username == request.user.username or request.user.is_staff:
        upload_.delete()

    return redirect('read_upload', pk)


def ReadUpload(request, pk=None):
    if pk is None:
        return render(request, 'NotFound.html')
    if not Upload.objects.filter(id=pk).exists():
        return render(request, 'NotFound.html')

    upload_ = Upload.objects.get(id=pk)

    if upload_.username.username == request.user.username:
        author = True
    else:
        author = False

    uploadedfile_ = UploadedFile.objects.filter(upload=upload_)

    # HOURS FOR DELETE
    delete_in = int((upload_.date_delete - upload_.date_upload).total_seconds() // 3600)
    # IF TIME END - 404
    if delete_in < 1:
        return render(request, 'NotFound.html')

    return render(request, 'APP_filehost/read_upload.html', {
        'upload': upload_,
        'files': uploadedfile_,
        'total_size': str(float(upload_.size) / 1024 / 1024)[0:6],
        'delete_in': delete_in,
        'domain': request.get_host(),
        'author': author
    })


def UploadFile(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = 'NULL'

    if username == 'NULL':
        DEFINED_SIZE = 6 * 1024 * 1024
    else:
        DEFINED_SIZE = 30 * 1024 * 1024

    if request.method == 'POST':
        # reCAPTCHA
        result_reCAPTCHA = reCAPTCHA_validation(request)
        if not result_reCAPTCHA['success'] and not request.user.is_staff:
            return render(request, 'APP_filehost/upload_file.html', context={
                'invalid': 'Invalid reCAPTCHA. Please try again.',
                'RECAPTCHA_KEY': env('GOOGLE_RECAPTCHA_SITE_KEY'),
                'DEFINED_SIZE': DEFINED_SIZE,
            })

        user_ = User.objects.get(username=username)
        files = dict(request.FILES.lists())['files[]']

        # CHECK SIZE
        total_size = 0
        for file in files:
            total_size += file.size
        if total_size > DEFINED_SIZE:
            if username == 'NULL':
                invalid = f'Files are more than {int(DEFINED_SIZE / 1024 / 1024)} MB in size. Register to increase the limit to 30 MB.'
            else:
                invalid = f'Files are more than {int(DEFINED_SIZE / 1024 / 1024)} MB in size.'
            return render(request, 'APP_filehost/upload_file.html', context={
                'RECAPTCHA_KEY': env('GOOGLE_RECAPTCHA_SITE_KEY'),
                'invalid': invalid,
                'DEFINED_SIZE': DEFINED_SIZE
            })

        # UPLOADING
        upload_ = Upload.objects.create(username=user_, size=total_size)
        upload_.save()
        for file in files:
            file_name = translit(str(file.name), language_code='ru', reversed=True).replace(' ', '_')
            log(f'FILENAME : {file_name}')
            uploadedfile_ = UploadedFile.objects.create(upload=upload_,
                                                        file=file,
                                                        file_size=file.size,
                                                        file_name=file_name)
            uploadedfile_.save()

        return render(request, 'APP_filehost/link_on_upload.html', context={
            'link': request.get_host() + request.get_full_path() + str(upload_.id)
        })

    return render(request, 'APP_filehost/upload_file.html', context={
        'RECAPTCHA_KEY': env('GOOGLE_RECAPTCHA_SITE_KEY'),
        'DEFINED_SIZE': DEFINED_SIZE
    })
