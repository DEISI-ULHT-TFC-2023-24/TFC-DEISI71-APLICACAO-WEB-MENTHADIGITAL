$(document).on("click", ".btn-submit-risk",  () => {
    //event.preventDefault();
    var idsSelecionados;
    var csrf_token = Cookies.get('csrftoken');
    var href = document.getElementById("risk-submit").getAttribute('data-href'); 
    temErros = false;
    data = new FormData();
    
    data.append('idade', document.getElementById('idade').value);

    data.append('sexo', document.getElementById('sexo').value);
    data.append('altura', document.getElementById('altura').value);
    data.append('peso', document.getElementById('peso').value);
    data.append('fumador', document.getElementById('fumador').value);
    data.append('horas_jejum', document.getElementById('horas_jejum').value);
    data.append('batimentos', document.getElementById('batimentos').value);
    
    
    data.append('pressao_arterial', document.getElementById('pressao_arterial').value);
    data.append('pressao_arterial_diastolica', document.getElementById('pressao_arterial_diastolica').value);

    
    data.append('colestrol_hdl', document.getElementById('colestrol_hdl').value);

    data.append('colestrol_nao_hdl', document.getElementById('colestrol_nao_hdl').value);
    data.append('colestrol_total', document.getElementById('colestrol_total').value);
    data.append('ldl',document.getElementById('ldl').value);
    data.append('tg', document.getElementById('tg').value); 
    data.append('cholhdl', document.getElementById('cholhdl').value);
    data.append('ifcc_hba1', document.getElementById('ifcc_hba1').value);
    data.append('ngsp_hba1', document.getElementById('ngsp_hba1').value);
    data.append('eag_hba1', document.getElementById('eag_hba1').value);

    data.append('diabetes', document.getElementById('diabetes').value);
    data.append('anos_diabetes', document.getElementById('anos_diabetes').value);
    data.append('enfarte', document.getElementById('enfarte').value);
    data.append('avc', document.getElementById('avc').value);
    data.append('doenca_pernas', document.getElementById('doenca_pernas').value);
    data.append('doenca_rins', document.getElementById('doenca_rins').value);
    data.append('hipercolestrol', document.getElementById('hipercolestrol').value);
    data.append('pat', document.getElementById('pat').value);
    data.append('pat_id_v2', document.getElementById('pat_id_v2').value);
    data.append('comentario', document.getElementById('comentario').value);
    data.append('recomendacoes', document.getElementById('recomendacoes').value);
    data.append('doenca_cognitiva', document.getElementById('doenca_cognitiva').value);
    data.append('pre_diabetico', document.getElementById('pre_diabetico').value);
    data.append('pergunta_cardiovascular', document.getElementById('pergunta_cardiovascular').value);
    


    
    // try {
    console.log("Tem_erros:", temErros)
    if (!temErros) {
        event.preventDefault();
        $.ajax({
            method: 'POST',
            url: href,
            data: data,
            mimeType: "multipart/form-data",
            headers: {'X-CSRFToken': csrf_token},
            contentType: false,
            processData: false,
            async: false,
            success: function (data) {
                console.log("Success!")
                $('.container-fluid').html(data);
                return false;
            },
            error: function () {
                console.log("Error!");
                alert("Pagina não disponível.");
            }
        })
    }
    // } catch (error) {
    //     console.error("Error:", error);
    // }$('.page-content').html(data);
});
