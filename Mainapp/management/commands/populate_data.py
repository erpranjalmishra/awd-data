from django.core.management.base import BaseCommand
from Mainapp.models import Sensordata
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Populate database with sample sensor data'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10, help='Number of records to create')

    def handle(self, *args, **options):
        count = options['count']
        
        # Clear existing data
        Sensordata.objects.all().delete()
        self.stdout.write(f'Cleared existing data')
        
        # Create sample data
        for i in range(count):
            # Generate realistic sensor data
            temp = round(20 + random.uniform(-5, 15), 1)
            humidity = round(40 + random.uniform(-10, 20), 1)
            ph = round(6.5 + random.uniform(-1, 1.5), 2)
            tds = round(300 + random.uniform(-100, 200), 1)
            o2 = round(random.uniform(85, 89), 1)
            
            # Create timestamp (recent data)
            timestamp = datetime.now() - timedelta(minutes=i*5)
            
            Sensordata.objects.create(
                deviceid="vikaspal@123",
                temp=temp,
                humidity=humidity,
                phvalue=ph,
                tds=tds,
                o2=o2,
                timestamp=timestamp
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {count} sensor records')
        )
