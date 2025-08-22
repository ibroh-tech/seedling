from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Check AgroEvent model and database structure'

    def handle(self, *args, **options):
        # Check model fields
        from seedling_app.models import AgroEvent
        self.stdout.write("AgroEvent model fields:")
        for field in AgroEvent._meta.fields:
            self.stdout.write(f"- {field.name}: {field.get_internal_type()}")
        
        # Check database columns
        self.stdout.write("\nDatabase columns:")
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'AgroEvent';
            """)
            for col in cursor.fetchall():
                self.stdout.write(f"- {col[0]}: {col[1]}")
        
        # Check if status_id exists
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT constraint_name, constraint_type 
                FROM information_schema.table_constraints 
                WHERE table_name = 'AgroEvent';
            """)
            self.stdout.write("\nTable constraints:")
            for constraint in cursor.fetchall():
                self.stdout.write(f"- {constraint[0]}: {constraint[1]}")
