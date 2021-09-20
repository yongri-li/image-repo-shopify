# image-repo-shopify

## Dependencies
    1. python
    2. Django
    3. Pillow
    4. django-cleanup
    5. python-decouple


## How to use
    1. clone repo using "git clone https://github.com/klenotiw/image-repo-shopify"
    2. install dependencies
        1. pip install django
        2. pip install python-decouple
        3. pip install django-cleanup
        4. pip install Pillow
    3. run env script
        - run the command "python3 gen_new_env.py" to generate a new .env file
        - this will generate you a django secret key so you can run the development server
        - the .env file will simply be a file name ".env" with a django secret key variable.
        - it will look something like this "SECRET_KEY = +q$k+$i0jbu=t(n6%s90idx%(6wzpozlocy8d+(_&&3jby_c)_"
    3. Run dev server using "python3 manage.py runserver"
    4. go to http://127.0.0.1:8000/ in your web browers and you will see the project. You can create an account, sign in and start looking through the features
    5. You can also use "python3 manage.py test" to run the test cases I made for development.

## Thanks
    Thanks for checking out my project. You should be able to see two test repositories called "Apollos Repo" and "All my Images". I found out about this internship opportunity a little late so excuse any rough edges. I had to make this in a week to make the deadline.


## Contact
    If you like my project or have any questions you can contact me at klenotiw@gmail.com or add me on linkedin at https://www.linkedin.com/in/bill-klenotiz/
