from django.db import models
import csv
from datetime import datetime

# create the Voter model
class Voter(models.Model):
    ''''''
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    street_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=50)
    precinct_number = models.CharField(max_length=10)
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)
    voter_score = models.IntegerField()

    def __str__(self):
        '''Return a string representation of the voter.'''
        return f"{self.first_name} {self.last_name} - Precinct {self.precinct_number}"
    

def load_data():
    '''Load data records from a CSV file into model instances'''   

    # Delete all existing records
    Voter.objects.all().delete()

    # Open the file for reading
    filename = '/Users/paulalburgos/Documents/BU/F24/cs412/newton_voters.csv'

    with open(filename, newline='') as f:
        reader = csv.reader(f)
        headers = next(reader)  # Skip the header row
        print(headers)

        # Loop to read all the lines in the file
        for fields in reader:
            try: 
                # Parse dates directly
                date_of_birth = fields[7].strip()
                date_of_registration = fields[8].strip()

                # Convert Boolean fields
                v20state = fields[11].strip().upper() == 'TRUE'
                v21town = fields[12].strip().upper() == 'TRUE'
                v21primary = fields[13].strip().upper() == 'TRUE'
                v22general = fields[14].strip().upper() == 'TRUE'
                v23town = fields[15].strip().upper() == 'TRUE'

                # Create a new instance of Voter with this record from CSV
                voter = Voter(
                    last_name=fields[1].strip(),
                    first_name=fields[2].strip(),
                    street_number=fields[3].strip(),
                    street_name=fields[4].strip(),
                    apartment_number=fields[5].strip() if fields[5].strip() else None,
                    zip_code=fields[6].strip(),
                    date_of_birth=date_of_birth,
                    date_of_registration=date_of_registration,
                    party_affiliation=fields[9].strip(),
                    precinct_number=fields[10].strip(),
                    v20state=v20state,
                    v21town=v21town,
                    v21primary=v21primary,
                    v22general=v22general,
                    v23town=v23town,
                    voter_score=int(fields[16].strip())
                )
                voter.save()
                print(f'Voter {voter} saved.')
                print(fields)
            except Exception as e:
                print(f'Error: Skipping record due to {e}')