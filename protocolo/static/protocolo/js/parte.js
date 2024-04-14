document.getElementById('btn-popup').addEventListener('click', () => {
    // console.log(document.getElementById('btn-popup'));
    // console.log(document.getElementById('wrapper-parts'));
    document.getElementById('wrapper-parts').style.display = 'block';
});

document.getElementById('btn-close').addEventListener('click', () => {
    document.getElementById('wrapper-parts').style.display = 'none';
});


var checkboxes = document.getElementsByClassName('part-checkbox');
for (var i = 0; i < checkboxes.length; i++) {
    checkboxes[i].addEventListener('click', (event) => {

        for (var i = 0; i < checkboxes.length; i++) {
            if (checkboxes[i].checked && checkboxes[i] != event.target) {
                checkboxes[i].checked = false;
            }
        }

    });
}



//funcao para adicionar uma nova part ao ParteDoUtilizador
$(document).on("click", "#btn-proxima-linha", async () => {
    var idsSelecionados;
    var csrf_token = Cookies.get('csrftoken');
    data = new FormData();
    data.append('patientId', document.getElementById('patientId').value);
    $('.part-checkbox').each(function () {
        if ($(this).is(':checked')) {
            data.append('partId', $(this).attr('value'));
        }
    });
    console.log('teste');
    console.log(data);
    try {
        const response = await fetch("atualizar-tabela", {
            method: "POST",
            body: data,
            headers: { 'X-CSRFToken': csrf_token },
        });
    } catch (error) {
        console.error("Error:", error);
    }
});


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// document.getElementById('risk-report').addEventListener('click', async () => {


// });
// document.getElementById('data_atual').value = new Date().toISOString();
