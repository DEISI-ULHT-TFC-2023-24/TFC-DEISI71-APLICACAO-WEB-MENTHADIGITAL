from django import template
from datetime import datetime

register = template.Library()


@register.filter
def convert(value):
    return value.encode('iso-8859-1').decode('iso-8859-1') if value else value


@register.simple_tag
def minimum(val1, val2):
    return min(val1, val2)


@register.simple_tag
def count(list):
    return len(list)


@register.simple_tag
def subtraction(val1, val2):
    return val1 - val2


@register.simple_tag
def abvd_evaluation(val):
    if val == 0:
        return "Nulo"
    elif val <= 7:
        return "Ligeiro"
    elif val <= 14:
        return "Moderado"
    elif val <= 19:
        return "Severo"
    elif val <= 24:
        return "Muito Severo"


@register.simple_tag
def aivd_evaluation(val, sex):
    if sex == 'Masculino':
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
    elif sex == 'Feminino':
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


@register.simple_tag
def hads_a_quotation(answers):
    q = 0
    for a in answers:
        if a.instrument == 'HADS':
            if a.question.order % 2 != 0:
                q = q + a.quotation
    return q


@register.simple_tag
def hads_d_quotation(answers):
    q = 0
    for a in answers:
        if a.instrument == 'HADS':
            if a.question.order % 2 == 0:
                q = q + a.quotation
    return q


@register.simple_tag
def hads_evaluation(quotation):
    if quotation <= 7:
        return "Normal"
    elif quotation <= 10:
        return "Ligeiro"
    elif quotation <= 14:
        return "Moderado"
    else:
        return "Severo"


@register.simple_tag
def bsi_somatizacao_quotation(answers):
    q = 0
    for a in answers:
        if a.instrument == 'BSI':
            if a.question.order in [2, 7, 23, 29, 30, 33, 37]:
                q = q + a.multiple_choice_answer.quotation
    return q


@register.simple_tag
def bsi_obs_comp_quotation(answers):
    q = 0
    for a in answers:
        if a.instrument == 'BSI':
            if a.question.order in [5, 15, 26, 27, 32, 36]:
                q = q + a.multiple_choice_answer.quotation
    return q


@register.simple_tag
def bsi_sens_interp_quotation(answers):
    q = 0
    for a in answers:
        if a.instrument == 'BSI':
            if a.question.order in [20, 21, 22, 42]:
                q = q + a.multiple_choice_answer.quotation
    return q


@register.simple_tag
def bsi_depressao_quotation(answers):
    q = 0
    for a in answers:
        if a.instrument == 'BSI':
            if a.question.order in [9, 16, 17, 18, 35, 50]:
                q = q + a.multiple_choice_answer.quotation
    return q


@register.simple_tag
def bsi_ansiedade_quotation(answers):
    q = 0
    for a in answers:
        if a.instrument == 'BSI':
            if a.question.order in [1, 12, 19, 38, 45, 49]:
                q = q + a.multiple_choice_answer.quotation
    return q


@register.simple_tag
def bsi_hostilidade_quotation(answers):
    q = 0
    for a in answers:
        if a.instrument == 'BSI':
            if a.question.order in [6, 13, 40, 41, 46]:
                q = q + a.multiple_choice_answer.quotation
    return q


@register.simple_tag
def bsi_ansiedade_fob_quotation(answers):
    q = 0
    for a in answers:
        if a.instrument == 'BSI':
            if a.question.order in [8, 28, 31, 43, 47]:
                q = q + a.multiple_choice_answer.quotation
    return q


@register.simple_tag
def bsi_ideacao_paranoide_quotation(answers):
    q = 0
    for a in answers:
        if a.instrument == 'BSI':
            if a.question.order in [4, 10, 24, 48, 51]:
                q = q + a.multiple_choice_answer.quotation
    return q


@register.simple_tag
def bsi_psicoticismo_quotation(answers):
    q = 0
    for a in answers:
        if a.instrument == 'BSI':
            if a.question.order in [3, 14, 34, 44, 53]:
                q = q + a.multiple_choice_answer.quotation
    return q

@register.simple_tag
def bsi_igs(answers):
    count = 0
    sum = 0
    for a in answers:
        if a.instrument == 'BSI':
            count += 1
            sum += a.quotation
    return sum/count

@register.simple_tag
def bsi_tsp(answers):
    count = 0
    for a in answers:
        if a.instrument == 'BSI':
            if a.quotation > 0:
                count += 1
    return count

@register.simple_tag
def bsi_isp(answers):
    count = 0
    sum = 0
    for a in answers:
        if a.instrument == 'BSI':
            if a.quotation > 0:
                count += 1
            sum += a.quotation
    return sum/count


@register.simple_tag
def gds_evaluation(answers):
    for a in answers:
        if a.instrument == 'GDS':
            if 'Estadio' in a.question.name:
                return f"Nível {a.quotation}: {a.multiple_choice_answer.name}"


@register.simple_tag
def exist_answers(instrument, answers):
    for a in answers:
        if a.instrument == instrument:
            return True


@register.simple_tag
def mmse_evaluation(patient, quotation):
    # True = Com declinio
    # False = Sem declinio
    if patient.escolaridade == 'Analfabeto':
        return quotation <= 15
    elif patient.escolaridade in ['1-4', '5-10', '11+']:
        return quotation <= 22
    else:
        return quotation <= 27


@register.simple_tag
def neoffi20_neuroticismo(answers):
    q = 0
    for a in answers:
        if a.instrument == 'NEO-FFI 20':
            if a.question.order in [1, 6, 11, 16]:
                q = q + a.multiple_choice_answer.quotation
    return q


@register.simple_tag
def neoffi20_extroversao(answers):
    q = 0
    for a in answers:
        if a.instrument == 'NEO-FFI 20':
            if a.question.order in [2, 7, 12, 17]:
                q = q + a.multiple_choice_answer.quotation
    return q


@register.simple_tag
def neoffi20_experiencia(answers):
    q = 0
    for a in answers:
        if a.instrument == 'NEO-FFI 20':
            if a.question.order in [3, 8, 13, 18]:
                q = q + a.multiple_choice_answer.quotation
    return q


@register.simple_tag
def neoffi20_amabilidade(answers):
    q = 0
    for a in answers:
        if a.instrument == 'NEO-FFI 20':
            if a.question.order in [4, 9, 14, 19]:
                q = q + a.multiple_choice_answer.quotation
    return q


@register.simple_tag
def neoffi20_conscienciosidade(answers):
    q = 0
    for a in answers:
        if a.instrument == 'NEO-FFI 20':
            if a.question.order in [5, 10, 15, 20]:
                q = q + a.multiple_choice_answer.quotation
    return q


@register.simple_tag
def get_area_id(instrument, part):
    for area in instrument.area.all():
        if area.part.get() == part:
            return area.id


@register.simple_tag
def chc_answers(answers):
    for a in answers:
        if a.instrument == 'None':
            if a.question.name in ['Consciência', 'Atividade Motora', 'Humor']:
                return True


@register.simple_tag
def chc_consciencia(answers):
    list = []
    for a in answers:
        if a.instrument == 'None':
            if a.question.name == 'Consciência':
                for mca in a.MCCAnswer.all():
                    list.append(mca.choice.name)
    return ", ".join(list)


@register.simple_tag
def chc_atividade_motora(answers):
    list = []
    for a in answers:
        if a.instrument == 'None':
            if a.question.name == 'Atividade Motora':
                for mca in a.MCCAnswer.all():
                    list.append(mca.choice.name)
    return ", ".join(list)


@register.simple_tag
def chc_humor(answers):
    list = []
    for a in answers:
        if a.instrument == 'None':
            if a.question.name == 'Humor':
                for mca in a.MCCAnswer.all():
                    list.append(mca.choice.name)
    return ", ".join(list)


@register.simple_tag
def cde(answers):
    for a in answers:
        if a.instrument == 'None':
            if a.question.name == 'Cooperação dada na entrevista':
                return a.multiple_choice_answer.name


@register.simple_tag
def rca(answers):
    for a in answers:
        if a.instrument == 'None':
            if a.question.name == 'Relação com o Avaliador':
                return a.multiple_choice_answer.name


@register.simple_tag
def save(x):
    return x


@register.simple_tag
def resolution_filter_get_percentage(resolutions, order, person,doctor):
    r = resolutions.filter(patient=person, part__order=order, doctor= doctor)
    
    print(r)

    if len(r) == 1:
        return r.get().statistics.get('total_percentage')
    else:
        return 0

@register.simple_tag
def get_part_id_from_resolutions(resolutions, order, person):
    r = resolutions.filter(patient=person, part__order=order)
    return r.get().part.id


@register.simple_tag
def truncated_second_word(text, max):
    t = text.split()
    final = text
    if len(t) > 1:
        word1 = t[0]
        last_word = t[-1]
        length_word2 = len(last_word)
        final = ""
        if length_word2 - max <= 0:
            final = word1[0] + "... " + last_word[0:9]
        elif length_word2 - max > 0:
            #print(max - length_word2)
            final = word1[0:abs(max - length_word2)] + "... " + last_word[0:9]

        if length_word2 > 9:
            final += "..."
    return final
@register.simple_tag
def area_from_question_and_part(q, part):
    for a in q.section.dimension.instrument.area.all():
        if a.instrument.area.part == part:
            return a

@register.simple_tag
def area_from_instrument_and_part(q, instrument):
    for a in q.section.dimension.instrument.area.all():
        if a.instrument == instrument:
            return a

@register.simple_tag
def get_area_from_id(areas, id):
    return 0
    return areas.get(id=id)

@register.simple_tag
def multiply(a, b):
    return a * b

@register.simple_tag
def get_if_done_from_percentage_list(percentages, id, area):
    return percentages.get(int(id)).get(area)

@register.simple_tag
def get_rowspan(rowspans, estadio):
   e = str(estadio).split(" - ")
   return rowspans.get(str(e[0])) + 1


@register.simple_tag
def get_from_answers_dict(dict, respondente, pergunta):
   return dict.get(str(respondente)).get(str(pergunta))

@register.simple_tag
def get_from_dict(dict, key):
   return dict.get(key)

@register.simple_tag
def len_dict(dict, key):
   return len(dict.get(key))

@register.simple_tag
def calculate_age(born):
    today = datetime.now()
    #print(today)
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day)) 


@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists() 