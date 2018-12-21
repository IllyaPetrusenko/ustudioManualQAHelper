import random
from faker import Faker

fake_data = Faker('ro_RO')

word = fake_data.word()
text = fake_data.text(120)


format_types_2 = []
dfnv = random.choice(format_types_2)

