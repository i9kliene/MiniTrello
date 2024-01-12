from django.db import models
from django.urls import reverse
from django.conf import settings


MAX_TITLE_LEN = 64
USER = settings.AUTH_USER_MODEL


class Board(models.Model):
    owner = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="owner")
    members = models.ManyToManyField(USER, blank=True, related_name="members")
    title = models.CharField(max_length=MAX_TITLE_LEN, blank=False, null=False)
    description = models.TextField(blank=True, null=False)
    # TODO: add section_limit field
    # === non-editable ===
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]
        constraints = [models.UniqueConstraint(fields=["title"], name="unique_title")]

    def __str__(self) -> str:
        return self.title

    @property
    def getMemberIDs(self):
        return [t.id for t in self.members.all()]

    def get_absolute_url(self):
        return reverse("board-index", args=[str(self.id)])

    # TODO
    # def save()


class Section(models.Model):
    title = models.CharField(max_length=MAX_TITLE_LEN, blank=False, null=False)
    description = models.TextField(blank=True, null=False)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    # TODO: add card_limit field
    # === non-editable ===
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    # dependent on the Card's completed field
    completed = models.BooleanField(default=False, editable=False)
    # we set this manually on the server based using a section value sent to the server
    section_order = models.PositiveIntegerField(
        default=0, editable=False, db_index=True
    )

    class Meta:
        ordering = ["section_order"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # This updates the date time field as well
        if self.board:
            self.board.save()


class Tag(models.Model):
    title = models.CharField(max_length=MAX_TITLE_LEN, blank=False, null=False)
    description = models.TextField(blank=True, null=False)
    # TODO: add color field
    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    class Meta:
        # check for the same board, same title should not possible
        constraints = [
            models.UniqueConstraint(
                fields=["title", "board"], name="unique_title_board"
            )
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # This updates the date time field as well
        if self.board:
            self.board.save()


class Card(models.Model):
    class Priority(models.IntegerChoices):
        HIGH = 1, "High"
        MEDIUM = 2, "Medium"
        LOW = 3, "Low"

    priority = models.IntegerField(choices=Priority.choices, default=Priority.MEDIUM)
    title = models.CharField(max_length=MAX_TITLE_LEN, blank=False, null=False)
    description = models.TextField(blank=True, null=False)
    tags = models.ManyToManyField(Tag, blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    deadline = models.DateField(blank=True, null=True)
    # === non-editable ===
    card_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    # TODO: Allow for sub-task in the card

    class Meta:
        ordering = ["card_order"]

    def __str__(self):
        return f"{self.id} - {self.title}"

    @property
    def getTagIDs(self):
        return [t.id for t in self.tags.all()]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.section:
            sec = Section.objects.get(id=self.section.id)
            if Card.objects.filter(section=sec, completed=False).count() == 0:
                print(
                    Card.objects.filter(section=sec, completed=False).count(),
                    self.section.id,
                )
                self.section.completed = True
            else:
                self.section.completed = False

            self.section.save()
