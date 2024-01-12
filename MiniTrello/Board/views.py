# == General imports ==
import json
from datetime import datetime
from os import path

# == Django imports ==
from django.http import HttpResponse, HttpResponseNotFound
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from . import models
from . import utils
from . import forms
from User.models import CustomUser

# ========= Board ===========


# https://stackoverflow.com/a/69655415
# Allow only board owner and members to view and update it content
def verify_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        board = models.Board.objects.get(id=kwargs["board_id"])
        if board.owner.id == request.user.id or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        elif request.user in board.members.all():
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrapper_func


@login_required(login_url="user-login")
def boardList(request):
    my_boards = models.Board.objects.filter(owner=request.user)
    member_boards = models.Board.objects.filter(members=request.user)
    context = {"my_boards": my_boards, "member_boards": member_boards}
    return render(request, template_name="Board/board_list.html", context=context)


@login_required(login_url="user-login")
def createBoard(request):
    form = forms.BoardForm()
    context = {}
    members = CustomUser.objects.all().exclude(id=request.user.id)
    context["members"] = members
    if request.method == "POST":
        form = forms.BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.owner = request.user
            board.save()
            return redirect("board-list")

    context["form"] = form
    return render(request, template_name="Board/add_board.html", context=context)


@login_required(login_url="user-login")
@verify_user
def updateBoard(request, board_id):
    board = models.Board.objects.get(id=board_id)
    # allow only board owner to update
    if board.owner.id != request.user.id and not request.user.is_superuser:
        raise PermissionDenied
    form = forms.BoardForm(instance=board)
    members = CustomUser.objects.all().exclude(id=request.user.id)
    context = {
        "board": board,
        "members": members,
    }

    if request.method == "POST":
        form = forms.BoardForm(request.POST, instance=board)
        if form.is_valid():
            form.save()
            return redirect("board-list")

    context["form"] = form
    return render(request, template_name="Board/update_board.html", context=context)


@login_required(login_url="user-login")
@verify_user
def deleteBoard(request, board_id):
    board = models.Board.objects.get(id=board_id)
    # allow only board owner to delete
    if board.owner.id != request.user.id and not request.user.is_superuser:
        raise PermissionDenied
    board = models.Board.objects.get(id=board_id)
    if request.method == "POST":
        board.delete()
        return redirect("board-list")
    return render(request, template_name="Board/delete_board.html")


# ========= End Board ===========

# ========= Section ===========


@login_required(login_url="user-login")
@verify_user
def boardIndex(request, board_id):
    sections = models.Section.objects.filter(board=board_id)
    tags = models.Tag.objects.filter(board=board_id)
    context = {"sections": sections, "tags": tags, "board_id": board_id}
    return render(request, template_name="Board/index.html", context=context)


@login_required(login_url="user-login")
@verify_user
def createSection(request, board_id):
    form = forms.SectionForm()
    context = {"board_id": board_id}
    if request.method == "POST":
        form = forms.SectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("board-index", board_id)

    context["form"] = form
    return render(request, template_name="Board/add_section.html", context=context)


@login_required(login_url="user-login")
@verify_user
def updateSection(request, board_id, section_id):
    section = models.Section.objects.get(id=section_id, board=board_id)
    form = forms.SectionForm(instance=section)
    context = {
        "section": section,
        "board_id": board_id,
    }

    if request.method == "POST":
        form = forms.SectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            return redirect("board-index", board_id)

    context["form"] = form
    return render(request, template_name="Board/update_section.html", context=context)


@login_required(login_url="user-login")
@verify_user
def deleteSection(request, board_id, section_id):
    section = models.Section.objects.get(id=section_id, board=board_id)
    context = {"board_id": board_id}
    if request.method == "POST":
        section.delete()
        return redirect("board-index", board_id)
    return render(request, template_name="Board/delete.html", context=context)


# ========= End Section ===========

# ========= Card ===========


@login_required(login_url="user-login")
@verify_user
def createCard(request, board_id, section_id):
    form = forms.CardForm()
    tags = models.Tag.objects.filter(board=board_id)
    priority_choices = models.Card._meta.get_field("priority").choices
    sections = models.Section.objects.filter(board=board_id)
    context = {
        "sections": sections,
        "tags": tags,
        "priority_choices": priority_choices,
        "section_id": section_id,
        "board_id": board_id,
    }

    if request.method == "POST":
        form = forms.CardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("board-index", board_id)

    context["form"] = form
    return render(request, template_name="Board/add_card.html", context=context)


@login_required(login_url="user-login")
@verify_user
def updateCard(request, board_id, card_id):
    card = models.Card.objects.get(id=card_id)
    if card.section.board.id != board_id:
        raise PermissionDenied
    form = forms.CardForm(instance=card)
    tags = models.Tag.objects.filter(board=board_id)
    priority_choices = models.Card._meta.get_field("priority").choices
    sections = models.Section.objects.filter(board=board_id)
    context = {
        "sections": sections,
        "tags": tags,
        "priority_choices": priority_choices,
        "card": card,
        "board_id": board_id,
    }

    if request.method == "POST":
        form = forms.CardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            return redirect("board-index", board_id)

    context["form"] = form
    return render(request, template_name="Board/update_card.html", context=context)


@login_required(login_url="user-login")
@verify_user
def deleteCard(request, board_id, card_id):
    card = models.Card.objects.get(id=card_id)
    if card.section.board.id != board_id:
        raise PermissionDenied
    context = {"board_id": board_id}
    if request.method == "POST":
        card.delete()
        return redirect("board-index", board_id)
    return render(request, template_name="Board/delete.html", context=context)


# ========= End Card ===========

# ========= Tag  ===========


@login_required(login_url="user-login")
@verify_user
def tagList(request, board_id):
    tags = models.Tag.objects.filter(board=board_id)
    context = {"tags": tags, "board_id": board_id}
    return render(request, template_name="Board/tags_list.html", context=context)


@login_required(login_url="user-login")
@verify_user
def createTag(request, board_id):
    form = forms.TagForm()
    context = {"board_id": board_id}
    if request.method == "POST":
        form = forms.TagForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("board-index", board_id)

    context["form"] = form
    return render(request, template_name="Board/add_tag.html", context=context)


@login_required(login_url="user-login")
@verify_user
def deleteTag(request, board_id, tag_id):
    tag = models.Tag.objects.get(id=tag_id, board=board_id)
    context = {"board_id": board_id}
    if request.method == "POST":
        tag.delete()
        return redirect("board-index", board_id)
    return render(request, template_name="Board/delete.html", context=context)


# ========= End Card ===========


def populateDB(request):
    if not settings.DEBUG:
        return HttpResponseNotFound
    CustomUser.objects.create_user(
        username="test1",
        password="test@abc",
        email="test1@user.com",
        first_name="Test1",
        last_name="Ln",
    )
    CustomUser.objects.create_user(
        username="test2",
        password="test@abc",
        email="test2@user.com",
        first_name="Test2",
        last_name="Ln",
    )
    CustomUser.objects.create_user(
        username="test3",
        password="test@abc",
        email="test3@user.com",
        first_name="Test3",
        last_name="Ln",
    )
    CustomUser.objects.create_user(
        username="test4",
        password="test@abc",
        email="test4@user.com",
        first_name="Test4",
        last_name="Ln",
    )
    json_file = path.abspath("../fixtures/board.json")
    utils.generate_data(json_file)
    file = open(json_file)
    json_object = json.load(file)
    if not models.Board.objects.all().exists():
        for data in json_object["Board"]:
            data["owner"] = CustomUser.objects.get(id=data["owner"])
            models.Board.objects.create(**data)

    if not models.Section.objects.all().exists():
        for data in json_object["Section"]:
            data["board"] = models.Board.objects.get(id=data["board"])
            models.Section.objects.create(**data)

    if not models.Tag.objects.all().exists():
        for data in json_object["Tag"]:
            data["board"] = models.Board.objects.get(id=data["board"])
            models.Tag.objects.create(**data)

    if not models.Card.objects.all().exists():
        for data in json_object["Card"]:
            data["section"] = models.Section.objects.get(id=data["section"])
            if "deadline" in data:
                date_format = "%Y-%m-%d"
                data["deadline"] = datetime.strptime(data["deadline"], date_format)
            temp_tag = data["tags"]
            del data["tags"]
            instance = models.Card.objects.create(**data)
            for val in temp_tag:
                instance.tags.add(models.Tag.objects.get(id=val))
    file.close()
    return HttpResponse("<h1>DB populated with dummy data</h1>")
