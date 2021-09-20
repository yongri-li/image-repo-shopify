from django.core.management.utils import get_random_secret_key

f = open(".env", "w")
f.write(f"SECRET_KEY = {get_random_secret_key()}")
f.close()
