"""@desc 
		Search's URL routes

 	@author 
 		Domnan Diretnan
 		Artificial Intelligence Enthusiast & Software Engineer.
 		Email: diretnandomnan@gmail.com
 		Github: https://github.com/deven96
 		GitLab: https://gitlab.com/Deven96

 	@project
 		@create date 2018-12-23 04:27:13
 		@modify date 2018-12-23 04:27:13

	@license
		MIT License
		Copyright (c) 2018. Domnan Diretnan. All rights reserved

 """

from django.urls import path
from ImageQ.search.views import IndexView

urlpatterns = [
	path('', IndexView.as_view())
]