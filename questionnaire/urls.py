from django.urls import path

from .views import *

urlpatterns = [
    path('home/', dashboard, name='home'),
    path('', dashboard, name='index'),
    path('new_questionnaire/', new_questionnaire, name='new_questionnaire'),
    path('new_section/', new_section, name='new_section'),
    path('new_question/', new_question, name='new_question'),
    #path('survey/', survey, name='survey'),
    path('survey/<int:questionnaire_id>/', survey, name='survey_view'),
    path('survey/<int:questionnaire_id>/section/<int:section_id>/', survey, name='survey_view'),
    path('survey/<int:questionnaire_id>/section/<int:section_id>/question/<int:question_id>/', survey, name='survey_view'),
    path('survey-complete/', survey_completed, name='survey_complete'),
    path('export/json/', export_surveys_json, name='export_surveys_json'),
    path('export/xml/', export_surveys_xml, name='export_surveys_xml'),
    path('export/pdf/', export_surveys_pdf, name='export_surveys_pdf'),
    path('export/excel/', export_surveys_excel, name='export_surveys_excel'),
]