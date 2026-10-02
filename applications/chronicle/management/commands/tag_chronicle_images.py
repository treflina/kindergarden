from django.core.management.base import BaseCommand
from django.db import transaction

from applications.chronicle.models import ChroniclePage
from applications.gallery.models import CustomImage


DEFAULT_TAG = "relacja"


class Command(BaseCommand):
    help = (
        "Adds a specified tag to all images used by ChroniclePage, "
        "including banner images and additional gallery images."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--tag",
            default=DEFAULT_TAG,
            help=f"Tag to add to the images (default: '{DEFAULT_TAG}').",
        )

        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be changed without modifying the database.",
        )

    def handle(self, *args, **options):
        tag_name = options["tag"].strip()
        dry_run = options["dry_run"]

        if not tag_name:
            self.stderr.write(
                self.style.ERROR("Tag name cannot be empty.")
            )
            return

        self.stdout.write("Searching for Chronicle images...")

        pages = ChroniclePage.objects.all()

        banner_ids = set()
        additional_ids = set()

        for page in pages:
            if page.banner_image_id:
                banner_ids.add(page.banner_image_id)

            for image_id in page.images.values_list("image_id", flat=True):
                if image_id:
                    additional_ids.add(image_id)

        image_ids = banner_ids | additional_ids

        images = CustomImage.objects.filter(id__in=image_ids)

        already_tagged = images.filter(tags__name=tag_name).count()
        to_tag = images.exclude(tags__name=tag_name)

        existing_image_ids = set(images.values_list("id", flat=True))
        missing_ids = image_ids - existing_image_ids

        self.stdout.write("")
        self.stdout.write("Chronicle image summary:")
        self.stdout.write(f"  Tag:                   {tag_name}")
        self.stdout.write(f"  Chronicle pages:       {pages.count()}")
        self.stdout.write(f"  Banner images:         {len(banner_ids)}")
        self.stdout.write(f"  Additional images:     {len(additional_ids)}")
        self.stdout.write(f"  Unique images:         {len(image_ids)}")
        self.stdout.write(f"  Already tagged:        {already_tagged}")
        self.stdout.write(f"  To be tagged:          {to_tag.count()}")

        if missing_ids:
            self.stdout.write(
                self.style.WARNING(
                    f"  Referenced images missing from database: "
                    f"{len(missing_ids)}"
                )
            )

        if not image_ids:
            self.stdout.write("")
            self.stdout.write("No Chronicle images found.")
            return

        if dry_run:
            self.stdout.write("")
            self.stdout.write(
                self.style.WARNING(
                    "DRY RUN: no changes have been made."
                )
            )
            return

        self.stdout.write("")
        confirmation = input(
            f"Add tag '{tag_name}' to {to_tag.count()} images? "
            "Type 'yes' to continue: "
        )

        if confirmation.lower() != "yes":
            self.stdout.write(
                self.style.WARNING(
                    "Operation cancelled. No changes were made."
                )
            )
            return

        tagged_count = 0

        with transaction.atomic():
            for image in to_tag.iterator():
                image.tags.add(tag_name)
                tagged_count += 1

        final_count = (
            CustomImage.objects
            .filter(
                id__in=image_ids,
                tags__name=tag_name,
            )
            .distinct()
            .count()
        )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully added '{tag_name}' to "
                f"{tagged_count} images."
            )
        )
        self.stdout.write(
            f"Images already tagged: {already_tagged}"
        )
        self.stdout.write(
            f"Total Chronicle images with '{tag_name}': {final_count}"
        )
