from django.shortcuts import render

# Create your views here.

def show_form(request):
    '''show the contact form'''

    template_name = "formdata/form.html"

    return render(request, template_name)


def submit(request):
    '''
    Handle the form submission
    Read the form data from the request and send it back to a template
    '''

    template_name = "formdata/confirmation.html"

    return render(request, template_name)

