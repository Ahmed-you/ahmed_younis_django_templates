# Student Profile

Django project for the Home Page and model assignment. Profiles are entered through Django admin and displayed on the Home Page with an uploaded image.

## Run the project

From the repository folder on Windows:

```powershell
cd project
py -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py createsuperuser
.\venv\Scripts\python.exe manage.py runserver
```

Open http://127.0.0.1:8000/ for the Home Page and http://127.0.0.1:8000/admin/ for administration. `/home/` and the previous `/index/` address also open the Home Page.

For the prepared local database, set a login password with `.\venv\Scripts\python.exe manage.py changepassword ahmed_admin`.

## Add a profile

1. Log in to admin with the account created above.
2. Under **Pages**, select **Student profiles**, then **Add student profile**.
3. Enter the full name, university ID number, age, date of birth, address and monthly salary in USD.
4. Upload an image. The included `examples/profile-avatar.png` can be used for the assignment.
5. Select **Save**, then open the Home Page.

The university ID is stored as text to preserve leading zeros. It must contain digits and be unique. Age must be between 1 and 120, date of birth cannot be in the future, and salary cannot be negative. Uploaded images are stored in `project/media/profiles/`.

## Included record

The screenshots use Ahmed Wael Younis, ID 120230395, age 22, born 12 June 2004, address Gaza. The monthly salary of USD 1,500.00 is a sample value, and the image is an illustrated avatar.

The local database and uploaded media are excluded from Git. To reproduce the included profile after migrating, run these commands from `project`:

```powershell
New-Item -ItemType Directory -Force media\profiles
Copy-Item ..\examples\profile-avatar.png media\profiles\profile-avatar.png
.\venv\Scripts\python.exe manage.py loaddata ..\examples\student_profiles.json
```

To create your own record through admin, follow the previous section instead of loading the fixture. Admin accounts are not included in the fixture.

## Verification

Run from `project`:

```powershell
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py test pages
.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

The six tests cover the empty Home Page, saved profile display and URL aliases, field validation, unique IDs, admin image upload and rejection of invalid image files. Browser checks also verify the uploaded photo and a mobile layout without horizontal overflow.

## Submission

- [Assignment report](output/pdf/student_profile_assignment.pdf)
- [Screenshots and migration output](docs/evidence/)
- [GitHub repository](https://github.com/Ahmed-you/ahmed_younis_django_templates)

This project uses Django's local development server. Uploaded media is served locally while `DEBUG` is enabled.
