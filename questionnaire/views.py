from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Section, Questionnaire, Question, Option, Survey, Response
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import TextBoxResponseForm, SingleChoiceResponseForm, MultipleChoiceResponseForm, LocationResponseForm
import json
from django.http import JsonResponse
from django.http import HttpResponse
from django.core.serializers import serialize
from django.template.loader import render_to_string

from xhtml2pdf import pisa
import pandas as pd


def export_surveys_excel(request):
    surveys = Survey.objects.prefetch_related('responses__question').all()
    data = []
    for survey in surveys:
        for response in survey.responses.all():
            data.append({
                'Survey ID': str(survey.uuid),
                'Question': response.question.question,
                'Answer': response.response
            })
    df = pd.DataFrame(data)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="surveys.xlsx"'
    df.to_excel(response, index=False)
    return response




def export_surveys_pdf(request):
    surveys = Survey.objects.prefetch_related('responses__question').all()
    html = render_to_string('surveys_pdf.html', {'surveys': surveys})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="surveys.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response


User = get_user_model()



def export_surveys_xml(request):
    surveys = Survey.objects.prefetch_related('responses__question').all()
    data = serialize('xml', surveys, use_natural_foreign_keys=True, use_natural_primary_keys=True)
    return HttpResponse(data, content_type='application/xml')



@login_required
def dashboard(request):
    questionnaires = Questionnaire.objects.all()
    sections = Section.objects.all()
    questions = Question.objects.all()
    surveys = Survey.objects.prefetch_related('responses__question').all()

    num_questionnaires = Questionnaire.objects.count()
    num_sections = Section.objects.count()
    num_questions = Question.objects.count()
    num_surveys = Response.objects.count()

    context = {
        'num_questionnaires': num_questionnaires,
        'num_sections': num_sections,
        'num_questions': num_questions,
        'num_surveys': num_surveys,
        'surveys': surveys,
        'page_title': "Urban Design Survey Questionnaire",
        'questionnaires': questionnaires,
        'sections': sections,
        'questions': questions,
        'current_user': request.user,
    }
    return render(request, 'index.html', context)

@login_required
def survey_completed(request):
    context = {
        'page_title': "Urban Design Survey Questionnaire",
        'current_user': request.user,
    }
    return render(request, 'survey_complete.html', context)

def get_response_form(question):
    if question.question_type == Question.TEXT_BOX:
        return TextBoxResponseForm
    elif question.question_type == Question.SINGLE_CHOICE:
        return SingleChoiceResponseForm
    elif question.question_type == Question.MULTIPLE_CHOICE:
        return MultipleChoiceResponseForm
    elif question.question_type == 4:  # Assuming 4 is for Location
        return LocationResponseForm


def survey(request, questionnaire_id, section_id=None, question_id=None):
    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
    sections = questionnaire.sections.all()
    
    if section_id is None:
        section = sections.first()
    else:
        section = get_object_or_404(Section, id=section_id)
    
    questions = section.questions.all()
    
    if question_id is None:
        question = questions.first()
    else:
        question = get_object_or_404(Question, id=question_id)
    
    ResponseForm = get_response_form(question)
    
    if request.method == 'POST':
        form = ResponseForm(request.POST, question=question)
        if form.is_valid():
            survey_id = request.session.get('survey_id')
            if not survey_id:
                survey = Survey.objects.create()
                request.session['survey_id'] = str(survey.uuid)
            else:
                survey = get_object_or_404(Survey, uuid=survey_id)
            
            response = form.save(commit=False)
            response.survey = survey
            response.question = question
            response.save()
            
            next_question = questions.filter(id__gt=question.id).first()
            if next_question:
                return redirect('survey_view', questionnaire_id=questionnaire.id, section_id=section.id, question_id=next_question.id)
            else:
                next_section = sections.filter(id__gt=section.id).first()
                if next_section:
                    return redirect('survey_view', questionnaire_id=questionnaire.id, section_id=next_section.id)
                else:
                    request.session.pop('survey_id', None)
                    return redirect('survey_complete')  # Redirect to a completion page
    else:
        form = ResponseForm(question=question)
    
    options = Option.objects.filter(question=question)
    
    context = {
        'questionnaire': questionnaire,
        'sections': sections,
        'section': section,
        'question': question,
        'form': form,
        'options': options,
    }
    return render(request, 'survey.html', context)


@login_required
def new_questionnaire(request):
    if request.method == 'POST':
        title = request.POST.get('questionnaire_title')
        description = request.POST.get('questionnaire_desc')
        
        if title and description:
            Questionnaire.objects.create(title=title, description=description, user=request.user)
            messages.success(request, 'Questionnaire added successfuly')
            return redirect('new_questionnaire')
        else:
            messages.error(request, 'Title and Description are required.')
            return redirect('new_questionnaire')
    context = {
        'page_title': "Add New Questionnaire",
        'current_user': request.user,
    }
    return render(request, 'new_questionnaire.html', context)

@login_required
def new_section(request):
    if request.method == 'POST':
        section_title = request.POST.get('section_title')
        section_desc = request.POST.get('section_desc')
        questionnaire_id = request.POST.get('questionnaire')
        
        if section_title and section_desc and questionnaire_id:
            try:
                questionnaire = Questionnaire.objects.get(id=questionnaire_id)
                Section.objects.create(
                    title=section_title,
                    description=section_desc,
                    questionnaire=questionnaire,
                    user=request.user
                )
                messages.success(request, 'Section added successfuly')
                return redirect('new_section')  # Redirect to a list of sections or another page
            except Questionnaire.DoesNotExist:
                messages.error(request, 'Selected questionnaire does not exist.')
                return redirect('new_section')
        else:
            return HttpResponse("All fields are required.", status=400)
    
    questionnaires = Questionnaire.objects.all()
    context = {
        'page_title': "Add New Section",
        'questionnaires': questionnaires,
        'current_user': request.user,
    }
    return render(request, 'new_section.html', context)

@login_required
def new_question(request):
    if request.method == 'POST':
        question_text = request.POST.get('question')
        question_mode = request.POST.get('question_mode')
        question_section_id = request.POST.get('question_section')
        single_choice_options = request.POST.get('question_mode_single')
        multiple_choice_options = request.POST.get('question_mode_multi')
        
        if question_text and question_mode and question_section_id:
            try:
                section = Section.objects.get(id=question_section_id)
                question = Question.objects.create(
                    question=question_text,  # Updated field name
                    question_type=question_mode,
                    section=section,
                    user=request.user
                )
                
                if question_mode == '2' and single_choice_options:
                    options = single_choice_options.split(',')
                    for option in options:
                        Option.objects.create(question=question, text=option.strip())
                
                if question_mode == '3' and multiple_choice_options:
                    options = multiple_choice_options.split(',')
                    for option in options:
                        Option.objects.create(question=question, text=option.strip())
                messages.success(request, 'Question added successfuly')
                return redirect('new_question')  # Redirect to a list of questions or another page
            except Section.DoesNotExist:
                messages.error(request, 'Selected section does not exist.')
                return redirect('new_question')
        else:
            messages.error(request, "All fields are required.")
            return redirect('new_question')
    
    sections = Section.objects.all()
    context = {
        'page_title': "Add New Question",
        'sections': sections,
        'current_user': request.user,
    }

    return render(request, 'new_question.html', context)



def export_surveys_json(request):
    surveys = Survey.objects.prefetch_related('responses__question').all()
    data = []
    for survey in surveys:
        survey_data = {
            'uuid': str(survey.uuid),
            'responses': [
                {
                    'question': response.question.question,
                    'answer': response.response
                } for response in survey.responses.all()
            ]
        }
        data.append(survey_data)
    return JsonResponse(data, safe=False)
