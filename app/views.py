from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from .models import infinido


FORM = """\n<ul><li> <div class="input-group mb-3">
<form class="form-inline" ><input type="hidden" name="parent" value="{}"><input class="form-control" type="text" name="title">
  <div class="input-group-append">
    <button class="btn" style="background:#481620 ; color:whitesmoke" type="submit">Add to Infilist</button>
  </div></div> </form> </li> </ul>"""
LAST_FORM = """\n<li> New List ? <form><input type="text" name="title"><input type="hidden" name="parent" value="-1"><input type=submit value="New Infilist"></form> </li>"""
DATA_LIST = "<li id={}>{}<a href='/done?id={}'>&nbsp&nbsp&nbsp&nbspDone</a><a href='/delete?id={}'>&nbsp&nbsp&nbsp&nbspDelete</a></li>"
OPEN_NEW_LIST = "<ul>"
CLOSE_OLD_LIST = "</ul>"
STRIKE_TAG_START = "<strike>"
STRIKE_TAG_END = "</strike>"


def delete(request):
    try:
        infinido.objects.all().filter(id=request.GET.get("id", "-3")).update(
            is_deleted=True
        )
    except:
        pass
    return HttpResponseRedirect("/")


def done(request):
    try:
        infinido.objects.all().filter(id=request.GET.get("id", "-3")).update(
            is_done=True
        )
    except:
        pass
    return HttpResponseRedirect("/")


def start_over(request):
    infinido.objects.all().delete()
    return HttpResponseRedirect("/")


def home(request):
    if "title" in request.GET.keys():
        infinido(
            title=request.GET.get("title", ""),
            parent=request.GET.get("parent", -1),
            content="",
        ).save()
        return HttpResponseRedirect("/")
    data = infinido.objects.all().filter(is_deleted=False)

    rendering_data = """ """
    data_stack = list(
        data.filter(parent=-1)
        .order_by("-id")
        .values_list("id", "title", "parent", "is_done")
    )
    oldparent = -1
    oldid = -1
    num_ul = 0
    while data_stack != []:
        stack_frame = data_stack.pop()
        if oldparent != stack_frame[2] and oldid != stack_frame[2]:
            rendering_data += CLOSE_OLD_LIST * num_ul
            num_ul = 0
        if oldid == stack_frame[2]:
            rendering_data += OPEN_NEW_LIST
            num_ul += 1
        if stack_frame[3]:  # Check if item is done
            rendering_data += STRIKE_TAG_START
        rendering_data += DATA_LIST.format(
            stack_frame[0], stack_frame[1], stack_frame[0], stack_frame[0]
        )
        if stack_frame[3]:  # Check if the item is done
            rendering_data += STRIKE_TAG_END
        rendering_data += FORM.format(stack_frame[0])
        rendering_data += "\n"
        oldid = stack_frame[0]
        oldparent = stack_frame[2]

        data_stack = data_stack + list(
            data.filter(parent=stack_frame[0])
            .order_by("id")
            .values_list("id", "title", "parent", "is_done")
        )
    rendering_data += CLOSE_OLD_LIST * num_ul
    rendering_data += LAST_FORM

    return render(request, "app.html", {"data": rendering_data})

