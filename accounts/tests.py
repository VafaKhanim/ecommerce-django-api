import os
import django

# Django konfiqurasiyasını yükləyin
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

# Django'nun authenticate funksiyasını import edin
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

# İstifadəçi adı və şifrəni burada daxil edin
username = 'vafa_admin'
password = '12.04.2005'

# authenticate() funksiyasını çağırın
user = authenticate(username=username, password=password)

# İstifadəçi tapıldıqda
if user is not None:
    print("User authenticated successfully")
else:
    print("Authentication failed")

    # Dəqiq problemi tapmaq üçün əlavə yoxlamalar
    try:
        # İstifadəçi adı ilə məlumatı tapmağa çalışın
        user_obj = User.objects.get(username=username)
        if user_obj.check_password(password):
            print("Password is correct, but authentication failed due to other reasons.")
        else:
            print("Password is incorrect.")
    except User.DoesNotExist:
        print(f"User with username '{username}' does not exist.")


