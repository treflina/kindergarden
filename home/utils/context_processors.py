from applications.todownload.models import ToDownloadPage

def todownloadpages_context(request):
    todownloadpages = ToDownloadPage.objects.live()
    return {'todownloadpages': todownloadpages}

