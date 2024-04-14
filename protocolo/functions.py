# Funções
import plotly.graph_objects as go
import plotly
import pandas as pd
from datetime import date
import plotly.io as pio
import io
import time

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def percentage(total: int, partial: int):
    '''
    Gets percentage from a total and partial number
    If the percentage is greater than 100%, it returns 100
    '''

    result = (partial / total) * 100
    return int(min(result, 100))


def create_percentage_list(obj_list, nr_answered):
    '''Returns a list of percentages, given a list of objects'''

    percentage = []
    for n, obj in enumerate(obj_list):
        p = 0
        if (n <= len(nr_answered)):
            if nr_answered[n] > 0 and obj.number_of_questions > 0:
                p = percentage(partial=nr_answered[n], total=obj.number_of_questions)
        percentage.append(int(p))
    return percentage


def print_nested_dict(dict_obj, indent=0):
    ''' Pretty Print nested dictionary with given indent level'''

    # Iterate over all key-value pairs of dictionary
    for key, value in dict_obj.items():
        # If value is dict type, then print nested dict
        if isinstance(value, dict):
            print(' ' * indent, key, ':', '{')
            print_nested_dict(value, indent + 4)
            print(' ' * indent, '}')
        else:
            print(' ' * indent, key, ':', value)

def bsi_somatizacao_quotation(answers):
    q = 0
    for a in answers:
        if a.instrument == 'BSI':
            if a.question.order in [2,7,23,29,30,33,37]:
                q = q + a.multiple_choice_answer.quotation
    return q

def bsi_obs_comp_quotation(answers):
    q = 0
    for a in answers:
        if a.instrument == 'BSI':
            if a.question.order in [5,15,26,27,32,36]:
                q = q + a.multiple_choice_answer.quotation
    return q

def bsi_sens_interp_quotation(answers):
    q = 0
    for a in answers:
        if a.instrument == 'BSI':
            if a.question.order in [20,21,22,42]:
                q = q + a.multiple_choice_answer.quotation
    return q

def bsi_depressao_quotation(answers):
    q = 0
    for a in answers:
        if a.instrument == 'BSI':
            if a.question.order in [9,16,17,18,35,50]:
                q = q + a.multiple_choice_answer.quotation
    return q

def bsi_ansiedade_quotation(answers):
    q = 0
    for a in answers:
        if a.instrument == 'BSI':
            if a.question.order in [1,12,19,38,45,49]:
                q = q + a.multiple_choice_answer.quotation
    return q

def bsi_hostilidade_quotation(answers):
    q = 0
    for a in answers:
        if a.instrument == 'BSI':
            if a.question.order in [6,13,40,41,46]:
                q = q + a.multiple_choice_answer.quotation
    return q

def bsi_ansiedade_fob_quotation(answers):
    q = 0
    for a in answers:
        if a.instrument == 'BSI':
            if a.question.order in [8,28,31,43,47]:
                q = q + a.multiple_choice_answer.quotation
    return q

def bsi_ideacao_paranoide_quotation(answers):
    q = 0
    for a in answers:
        if a.instrument == 'BSI':
            if a.question.order in [4,10,24,48,51]:
                q = q + a.multiple_choice_answer.quotation
    return q

def bsi_psicoticismo_quotation(answers):
    q = 0
    for a in answers:
        if a.instrument == 'BSI':
            if a.question.order in [3,14,34,44,53]:
                q = q + a.multiple_choice_answer.quotation
    return q

def bsi_quotation(a):
    return [bsi_somatizacao_quotation(a),bsi_obs_comp_quotation(a),bsi_depressao_quotation(a),
            bsi_sens_interp_quotation(a),bsi_ansiedade_quotation(a),bsi_hostilidade_quotation(a),
            bsi_ansiedade_fob_quotation(a),bsi_ideacao_paranoide_quotation(a),bsi_psicoticismo_quotation(a)]

def neoffi20_neuroticismo(answers):
    q = 0
    for a in answers:
        if a.instrument == 'NEO-FFI 20':
            if a.question.order in [1,6,11,16]:
                q = q + a.multiple_choice_answer.quotation
    return q

def neoffi20_extroversao(answers):
    q = 0
    for a in answers:
        if a.instrument == 'NEO-FFI 20':
            if a.question.order in [2,7,12,17]:
                q = q + a.multiple_choice_answer.quotation
    return q

def neoffi20_experiencia(answers):
    q = 0
    for a in answers:
        if a.instrument == 'NEO-FFI 20':
            if a.question.order in [3,8,13,18]:
                q = q + a.multiple_choice_answer.quotation
    return q

def neoffi20_amabilidade(answers):
    q = 0
    for a in answers:
        if a.instrument == 'NEO-FFI 20':
            if a.question.order in [4,9,14,19]:
                q = q + a.multiple_choice_answer.quotation
    return q

def neoffi20_conscienciosidade(answers):
    q = 0
    for a in answers:
        if a.instrument == 'NEO-FFI 20':
            if a.question.order in [5,10,15,20]:
                q = q + a.multiple_choice_answer.quotation
    return q

def make_graph(names, quotations, min, max):
    start_time = time.time()
    
    tick = 0
    if max < 10:    
        tick = 1
    else:
        tick = 5
    fig = go.Figure(data=go.Scatterpolar(
        r=quotations,
        theta=names,
        fill='toself'
    ))

    fig.update_traces(fill='toself')
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        width=425,
        height=200,
        margin=dict(l=70, r=70, t=20, b=20),
        dragmode=False,
        polar=dict(
            radialaxis=dict(
                tickmode='linear',
                tick0=0,
                dtick=tick,
                visible=True,
                range = [min, max]
                # https://plotly.com/python/radar-chart/
            ),
        ),
        showlegend=False
    )
    fig.update_xaxes(fixedrange=True)
    fig.update_yaxes(automargin=True, fixedrange=True)
    svg = plotly.offline.plot(fig, auto_open=False, output_type="div")
    buffer = io.BytesIO()
    fig.write_image(buffer, format='png', scale=1)
    buffer.seek(0)

    end_time = time.time()
    print(f"Took {end_time - start_time} to generate Graph")

    return svg, buffer

def calculate_timer_quotation(question, i):
    if not "Animais" in question.name:
        if i < 2:
            return 0
        elif i <= 3:
            return 1
        elif i <= 5:
            return 2
        elif i <= 7:
            return 3
        elif i <= 10:
            return 4
        elif i <= 13:
            return 5
        elif i <= 17:
            return 6
        elif i > 17:
            return 7
    else:
        if i < 5:
            return 0
        elif i <= 6:
            return 1
        elif i <= 8:
            return 2
        elif i <= 10:
            return 3
        elif i <= 13:
            return 4
        elif i <= 16:
            return 5
        elif i <= 21:
            return 6
        elif i > 21:
            return 7
        
def calculate_aivd_evaluation_men(val):
        if val == 0:
            return "Total"
        elif val <= 1:
            return "Grave"
        elif val <= 3:
            return "Moderada"
        elif val <= 4:
            return "Ligeira"
        else:
            return "Independente"
    
def calculate_aivd_evaluation_women(val):
    if val <= 1:
        return "Total"
    elif val <= 3:
        return "Grave"
    elif val <= 5:
        return "Moderada"
    elif val <= 7:
        return "Ligeira"
    else:
        return "Independente"
    

def hads_anxiety_quotation(answers):
    q = 0
    for a in answers:
        if a.instrument == 'HADS':
            if a.question.order % 2 != 0:
                q = q + a.quotation
    return q


def hads_depression_quotation(answers):
    q = 0
    for a in answers:
        if a.instrument == 'HADS':
            if a.question.order % 2 == 0:
                q = q + a.quotation
    return q

def hads_evaluation(quotation):
    if quotation <= 7:
        return "Normal"
    elif quotation <= 10:
        return "Ligeiro"
    elif quotation <= 14:
        return "Moderado"
    else:
        return "Severo"
    
def mmse_evaluation(patient, quotation):
    # True = Com declinio
    # False = Sem declinio
    if patient.escolaridade == 'Analfabeto':
        return quotation <= 15
    elif patient.escolaridade in ['1-4', '5-10', '11+']:
        return quotation <= 22
    else:
        return quotation <= 27