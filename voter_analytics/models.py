from django.db import models

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

    # delete all records
    Voter.objects.all().delete()

    # open the file for reading
    filename = '/Users/paulalburgos/Documents/BU/F24/cs412/newton_voters.csv'

    f = open(filename)
    headers = f.readline() # read/discard the headers
    print(headers)

    # loop to read all the lines in the file
    for line in f:
        # provide some protection around code that might generate an exception
        try: 
            fields = line.split(',') # create a list of fields

            # create a new instance of Voter object with this record from CSV
            voter = Voter(last_name=fields[0],
                        first_name=fields[1],
                        street_number=fields[2],
                        street_name=fields[3],
                        apartment_number=fields[4],
                        zip_code=fields[5],
                        date_of_birth=fields[6],
                        date_of_registration=fields[7],
                        party_affiliation=fields[8],
                        precinct_number=fields[9],
                        v20state=fields[10],
                        v21town=fields[11],
                        v21primary=fields[12],
                        v22general=fields[13],
                        v23town=fields[14],
                        voter_score=fields[15])
            voter.save()
            print(f'Voter {voter} saved.')
        except Exception as e:
            print(f'Error: {e}')
