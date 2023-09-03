from wagtail import blocks

class ScheduleBlock(blocks.StructBlock):
    start_hour = blocks.TimeBlock(label="Od", required=True)
    end_hour = blocks.TimeBlock(label="Do", required=True)
    description = blocks.TextBlock(label="Opis", required=True)

    class Meta: # noqa
        label = "Punkt planu dnia"
        icon = "edit"

