from django.urls import path
from . import views

urlpatterns = [
    path("boards/index/", views.boardList, name="board-list"),
    path("boards/add-board/", views.createBoard, name="create-board"),
    path("boards/<int:board_id>/update-board/", views.updateBoard, name="update-board"),
    path("boards/<int:board_id>/delete-board/", views.deleteBoard, name="delete-board"),
    path("boards/<int:board_id>/", views.boardIndex, name="board-index"),
    # Card urls
    path(
        "boards/<int:board_id>/create-card/<int:section_id>/",
        views.createCard,
        name="create-card",
    ),
    path(
        "boards/<int:board_id>/update-card/<int:card_id>/",
        views.updateCard,
        name="update-card",
    ),
    path(
        "boards/<int:board_id>/delete-card/<int:card_id>/",
        views.deleteCard,
        name="delete-card",
    ),
    # Section urls
    path(
        "boards/<int:board_id>/create-section/",
        views.createSection,
        name="create-section",
    ),
    path(
        "boards/<int:board_id>/update-section/<int:section_id>",
        views.updateSection,
        name="update-section",
    ),
    path(
        "boards/<int:board_id>/delete-section/<int:section_id>/",
        views.deleteSection,
        name="delete-section",
    ),
    path("boards/<int:board_id>/tags/", views.tagList, name="tag-list"),
    path("boards/<int:board_id>/tags/create", views.createTag, name="create-tag"),
    path(
        "boards/<int:board_id>/tags/delete/<int:tag_id>",
        views.deleteTag,
        name="delete-tag",
    ),
    # TODO: Debug mode only. Remove from production
    path("populate/", views.populateDB, name="populate-db"),
]
