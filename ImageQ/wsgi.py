"""@desc 
		WSGI config for django_api project.
        It exposes the WSGI callable as a module-level variable named ``application``.

 	@author 
 		Domnan Diretnan
 		Artificial Intelligence Enthusiast & Software Engineer.
 		Email: diretnandomnan@gmail.com
 		Github: https://github.com/deven96
 		GitLab: https://gitlab.com/Deven96

 	@project
 		@create date 2018-12-23 03:13:14
 		@modify date 2018-12-23 03:13:14

	@license
		MIT License
		Copyright (c) 2018. Diretnan Domnan. All rights reserved

 """


import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ImageQ.settings.common')

application = get_wsgi_application()
