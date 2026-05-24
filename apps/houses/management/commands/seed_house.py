from django.core.management.base import BaseCommand
from apps.houses.models import House


class Command(BaseCommand):
    help = "Create default houses for Molinari Forge"

    def handle(self, *args, **kwargs):

        houses = [
            {
                "name": "Netstorm",
                "color": "#3b82f6",
                "icon": "bi-lightning",
            },
            {
                "name": "Byteon",
                "color": "#8b5cf6",
                "icon": "bi-cpu",
            },
            {
                "name": "Algoritmia",
                "color": "#10b981",
                "icon": "bi-diagram-3",
            },
            {
                "name": "Cryptoria",
                "color": "#f59e0b",
                "icon": "bi-shield-lock",
            },
        ]

        for h in houses:
            obj, created = House.objects.get_or_create(
                name=h["name"],
                defaults={
                    "color": h["color"],
                    "motto": ""
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Created house {h['name']}"))
            else:
                self.stdout.write(f"House {h['name']} already exists")