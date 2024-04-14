var menuAtivo;

function ativaBotaoParticipante(idParticipante) {
    // desativa todos os botões
    desativaBotoesParticipantesEGrupo();
    //mostra botao respostas
    let buttonAnswer = document.querySelector('[data-menu="respostas"]');
    buttonAnswer.style.display = "block";
    //esconde botao presencas
    let buttonPresences = document.querySelector('[data-menu="presencas"]');
    buttonPresences.style.display = "none";
    // desativa o botao do grupo
    document.querySelectorAll(".grupo button").forEach((button) => {
        button.style.backgroundColor = "white";
        button.style.color = "black";
        button.style.font_weight = "600";
    });
    // obtém e ativa o botão do participante
    let buttonAtivo = document.querySelector(`[data-participante="${idParticipante}"]`);
    buttonAtivo.classList.add("selecionado");
}

function desativaBotoesParticipantesEGrupo(){
    // desativa todos os botões de participante e grupo
    document.querySelectorAll(".participante").forEach((button) => {
        button.classList.remove("selecionado");
    });
}

function desativaBotoesMenu(){
    // desativa todos os botões de participante e grupo

    document.querySelectorAll(".menu").forEach((button) => {
        document.querySelector(`#${button.dataset.menu}`).style.display = "none";
        button.classList.remove("selecionado");
    });
}

//Grupo
function ativaBotaoGrupo() {
    // desativa todos os botões
    desativaBotoesParticipantesEGrupo();
    // obtém e ativa o botão do grupo
    let buttonAtivo = document.querySelector(`[id="botao-grupo"]`);
    buttonAtivo.classList.add("selecionado");
    let buttonPresences = document.querySelector('[data-menu="presencas"]');
    buttonPresences.style.display = "block";
    //esconde botao respostas
    let buttonAnswer = document.querySelector('[data-menu="respostas"]');
    buttonAnswer.style.display = "none";
}

//Fim grupo
function ativaMenu() {
    // põe botões de menu a branco + esconde respetiva info
    desativaBotoesMenu();

    menuAtivo.classList.add("selecionado");

    document.querySelector(`#${menuAtivo.dataset.menu}`).style.display = "block";
}


function descarregaInfoParticipante(idSG, idParticipante) {
    /* vai buscar a informação do participante id */
    fetch('/diario/diario_participante/' + idSG + '/' + idParticipante)
        .then(response => response.text())
        .then(text => document.querySelector('.info').innerHTML = text)
        .then(() => ativaMenu());
}

//Grupo
function descarregaInfoGrupo(idSessaoGrupo) {
    /* vai buscar a informação do grupo id */
    fetch("/diario/diario_grupo/" + idSessaoGrupo)
        .then((response) => response.text())
        .then((text) => {
            document.querySelector(".info").innerHTML = text;
            //console.log(text)
        })
        .then(() => ativaMenu());
}

/***************************************************************************/
/********** DOMContentLoaded ***********************************************/
/***************************************************************************/
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".participantes button, .menu, button.grupo").forEach((button) => {
        button.classList.add("btn-diario")
    });

    var participante_logado = document.getElementById("participante_notas");
    menuAtivo = document.querySelector("[data-menu='notas']");

    if (participante_logado) {
        document.querySelectorAll(".menu").forEach((botaoParticipante) => {
            botaoParticipante.onclick = () => {
                descarregaInfoParticipante(participante_logado.dataset.sessaogrupo, participante_logado.dataset.participante);
                menuAtivo = botaoParticipante;
                ativaMenu();
            };
        });
    } else {
        document.querySelector("[data-menu='respostas']").style.display = "none";
        // onclick num participante
        document
            .querySelectorAll(".participantes button")
            .forEach((botaoParticipante) => {
                botaoParticipante.onclick = () => {
                    ativaBotaoParticipante(botaoParticipante.dataset.participante);
                    descarregaInfoParticipante(botaoParticipante.dataset.sessaogrupo, botaoParticipante.dataset.participante);
                };
            });
        //Grupo
        // onclick num grupo
        document.querySelectorAll(".grupo button").forEach((botaoGrupo) => {
            ativaBotaoGrupo(botaoGrupo.dataset.idgrupo);
            descarregaInfoGrupo(botaoGrupo.dataset.idgrupo);

            botaoGrupo.onclick = () => {
                ativaBotaoGrupo(botaoGrupo.dataset.idgrupo);
                descarregaInfoGrupo(botaoGrupo.dataset.idgrupo);
            };
        });
        // onclick num botão de menu
        document.querySelectorAll(".menu").forEach((menu) => {
            menu.onclick = () => {
                menuAtivo = menu;
                ativaMenu();
            };
        });
    }


});

/* vai buscar ao formulario com id formId
os dados e envia para servidor,
e espera por info atualizada do participante */
function sendFormParticipante(idSG, idPart, formId) {
    console.log("sendFormParticipante");
    let data = new FormData(document.getElementById(formId));
    fetch(`/diario/diario_participante/${idSG}/${idPart}`, {method: "POST", body: data})
        .then(response => response.text())
        .then(text => {
            document.querySelector('.info').innerHTML = text;
            ativaMenu();
            ativaBotaoParticipante(idPart);
        });
}

function sendForm(idSG, formId) {
    let data = new FormData(document.getElementById(formId));
    fetch(`/diario/diario_grupo/${idSG}`, {method: "POST", body: data})
        .then((response) => response.text())
        .then(text => {
            document.querySelector('.info').innerHTML = text;
            ativaMenu();
            ativaBotaoGrupo();
        });
}

function mostraDiarioBordo() {
    var htmlShow = document.getElementById("direita");

    if (htmlShow.style.display === "none") {
        htmlShow.style.display = "block";
    } else {
        htmlShow.style.display = "none";
    }
}

function calcula_percentagem(current, max) {
    return Math.trunc(current * 100 / max);
}

function ativa_partilha(sessaoGrupo_id) {
    document.querySelectorAll('li').forEach((li) => {
        li.classList.remove('partilhado');
    });

    obj = document.querySelector('li.active');
    id_parte = obj.dataset.parte;
    console.log(id_parte);
    obj.classList.add("partilhado");

    fetch('/diario/partilha_parte/' + sessaoGrupo_id + '/' + id_parte, {
        method: "GET",
    })
}


function atualizaPresencas(id) {
    let data = new FormData();
    var ele = document.getElementsByTagName('input');
    for (i = 0; i < ele.length; i++) {
        if (ele[i].type == "radio") {
            if (ele[i].checked) {
                data.append('nome', ele[i].name);
                data.append('valor', ele[i].value);
            }
        }
    }
    csrfmiddlewaretoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    data.append('csrfmiddlewaretoken', csrfmiddlewaretoken);

    fetch('/diario/atualizaPresencasDiario/' + id, {
        method: "POST",
        body: data
    })
        .then(response => response);
}

function submete_texto(sg_id, pg_id, participante_id) {
    document.querySelectorAll("textarea.pergunta, input.pergunta").forEach((i) => {
        if (i.value.length > 0 && i.type != "radio") {
            let data = new FormData();
            resposta = i.value;
            pergunta_id = i.nextElementSibling.innerHTML;
            parte_id = i.nextElementSibling.nextElementSibling.innerHTML;
            csrfmiddlewaretoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
            data.append('csrfmiddlewaretoken', csrfmiddlewaretoken);
            data.append('resposta_escrita', resposta);
            //console.log("Fetching: " + '/diario/guarda_resposta/' + sg_id + '/' + pg_id + '/' + participante_id + '/' + pergunta_id);
            fetch('/diario/guarda_resposta/' + sg_id + '/' + pg_id + '/' + participante_id + '/' + pergunta_id + '/' + parte_id, {
                method: "POST",
                body: data,
            })
        }
    });
}

function submete_ficheiros(sg_id, pg_id, participante_id) {
    document.querySelectorAll("input[type='file']").forEach((i) => {
        if (i.value.length > 0) {
            let formData = new FormData();
            formData.append("file", i.files[0]);
            pergunta_id = i.nextElementSibling.innerHTML;
            parte_id = i.nextElementSibling.nextElementSibling.innerHTML;
            csrfmiddlewaretoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
            formData.append('csrfmiddlewaretoken', csrfmiddlewaretoken);

            fetch('/diario/guarda_resposta/' + sg_id + '/' + pg_id + '/' + participante_id + '/' + pergunta_id + '/' + parte_id, {
                method: "POST",
                body: formData
            });
        }
    });
}

function submete_radio(sg_id, pg_id, participante_id) {
    document.querySelectorAll("input[type='radio']:checked").forEach((i) => {
        //console.log("radio");
        if (i.value.length > 0) {
            let formData = new FormData();
            resposta = i.value
            formData.append('choice', resposta)
            pergunta_id = i.nextElementSibling.innerHTML;
            parte_id = i.nextElementSibling.nextElementSibling.innerHTML;
            csrfmiddlewaretoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
            formData.append('csrfmiddlewaretoken', csrfmiddlewaretoken);

            fetch('/diario/guarda_resposta/' + sg_id + '/' + pg_id + '/' + participante_id + '/' + pergunta_id + '/' + parte_id, {
                method: "POST",
                body: formData
            });
        }
    });
}


function submete(sg_id, pg_id, participante_id) {
    submete_texto(sg_id, pg_id, participante_id);
    submete_ficheiros(sg_id, pg_id, participante_id);
    submete_radio(sg_id, pg_id, participante_id);
}


function submete_texto_diario(sg_id, participante_id) {
    document.querySelectorAll("textarea.pergunta, input.pergunta").forEach((i) => {
        if (i.value.length > 0 && i.type != "radio" && i.type != "checkbox") {
            checkbox = i.parentElement.nextElementSibling.children[0].checked;
            let data = new FormData();
            resposta = i.value;
            pergunta_id = i.nextElementSibling.dataset.perguntaid;
            parte_id = i.nextElementSibling.dataset.parteid;
            pg_id = i.nextElementSibling.dataset.partegrupoid;
            csrfmiddlewaretoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
            data.append('csrfmiddlewaretoken', csrfmiddlewaretoken);
            data.append('resposta_escrita', resposta);
            if (checkbox) {
                data.append('certo', 'true');
            } else {
                data.append('certo', 'false');
            }
            //console.log("Fetching: " + '/diario/guarda_resposta/' + sg_id + '/' + pg_id + '/' + participante_id + '/' + pergunta_id);
            fetch('/diario/guarda_resposta/' + sg_id + '/' + pg_id + '/' + participante_id + '/' + pergunta_id + '/' + parte_id, {
                method: "POST",
                body: data,
            })
        }
    });
}

function submete_ficheiros_diario(sg_id, participante_id) {
    document.querySelectorAll("input[type='file']").forEach((i) => {
        if (i.value.length > 0) {
            let formData = new FormData();
            formData.append("file", i.files[0]);
            pergunta_id = i.nextElementSibling.innerHTML.dataset.perguntaid;
            parte_id = i.nextElementSibling.innerHTML.dataset.parteid;
            pg_id = i.nextElementSibling.innerHTML.dataset.partegrupoid;
            csrfmiddlewaretoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
            checkbox = i.parentElement.nextElementSibling.children[0].checked;
            if (checkbox) {
                formData.append('certo', 'true');
            } else {
                formData.append('certo', 'false');
            }
            formData.append('csrfmiddlewaretoken', csrfmiddlewaretoken);

            fetch('/diario/guarda_resposta/' + sg_id + '/' + pg_id + '/' + participante_id + '/' + pergunta_id + '/' + parte_id, {
                method: "POST",
                body: formData
            });
        }
    });
}

function submete_radio_diario(sg_id, participante_id) {
    document.querySelectorAll("input[type='radio']:checked").forEach((i) => {
        //console.log("radio");
        if (i.value.length > 0) {
            let formData = new FormData();
            resposta = i.value;
            checkbox = i.parentElement.nextElementSibling.children[0].checked;
            formData.append('choice', resposta);
            if (checkbox) {
                formData.append('certo', 'true');
            } else {
                formData.append('certo', 'false');
            }
            pergunta_id = i.nextElementSibling.innerHTML.dataset.perguntaid;
            parte_id = i.nextElementSibling.innerHTML.dataset.parteid;
            pg_id = i.nextElementSibling.innerHTML.dataset.partegrupoid;
            csrfmiddlewaretoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
            formData.append('csrfmiddlewaretoken', csrfmiddlewaretoken);

            fetch('/diario/guarda_resposta/' + sg_id + '/' + pg_id + '/' + participante_id + '/' + pergunta_id + '/' + parte_id, {
                method: "POST",
                body: formData
            });
        }
    });
}

function valida_partilha(partilha_id) {
    var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    fetch(`/diario/complete_partilha/${partilha_id}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
    })
    .then(response => {response.json();
        console.log(response.json())
    }
    )
    .then(data => {
        window.location.reload();
    });
}

function elimina_partilha(partilha_id) {
    var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    fetch(`/diario/remove_partilha/${partilha_id}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response, if needed
        // You can add a page reload here to update the page after the removal
        window.location.reload();
    });
}


function submete_diario(sg_id, participante_id) {
    console.log("diario");
    submete_texto_diario(sg_id, participante_id);
    submete_ficheiros_diario(sg_id, participante_id);
    submete_radio_diario(sg_id, participante_id);
}

// function submete_avaliacao(sg_id){
//   event.preventDefault();
//   var participante_list = [];
//   var interesse_list = [];
//   var comunicacao_list = [];
//   var iniciativa_list = [];
//   var satisfacao_list = [];
//   var humor_list = [];
//   var eficacia_relacional_list = [];
//   var observacoes;
//   document.querySelectorAll(".avaliacao_participante").forEach((i) => {
//     if (i.name == "participante"){
//         participante_list.push(i.value);
//     }
//     if (i.name == "interesse"){
//       interesse_list.push(i.value);
//     }
//     if (i.name == "comunicacao"){
//       comunicacao_list.push(i.value);
//     }
//     if (i.name == "iniciativa"){
//       iniciativa_list.push(i.value);
//     }
//     if (i.name == "satisfacao"){
//       satisfacao_list.push(i.value);
//     }
//     if (i.name == "humor"){
//       humor_list.push(i.value);
//     }
//     if (i.name == "eficacia_relacional"){
//         eficacia_relacional_list.push(i.value);
//     }
//   });

//   observacao = document.querySelector('#obs_part').value

//     for (let i = 0; i < participante_list.length - 1; i++) {
//       formData = new FormData();
//       csrfmiddlewaretoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
//       formData.append('csrfmiddlewaretoken',csrfmiddlewaretoken);
//       formData.append('participante', participante_list[i]);
//       formData.append('interesse', interesse_list[i]);
//       formData.append('comunicacao', comunicacao_list[i]);
//       formData.append('iniciativa', iniciativa_list[i]);
//       formData.append('satisfacao', satisfacao_list[i]);
//       formData.append('humor', humor_list[i]);
//       formData.append('eficacia_relacional', eficacia_relacional_list[i]);
//       formData.append('observacao', observacao )
//       fetch('/diario/guarda_avaliacao_participante/' + sg_id, {
//         method: "POST",
//         body: formData,
//       });
//     }
// }

//Na criação de um novo grupo
const programa = document.querySelector('#programa');

programa.addEventListener('change', (event) => {
    console.log("switch");
    switch (programa) {
        case 'CARE':
            document.querySelector('.filtro_care').style.display = block;
            document.querySelector('.filtro_cog').style.display = hidden;
            break;
        case 'COG':
            document.querySelector('.filtro_care').style.display = hidden;
            document.querySelector('.filtro_cog').style.display = block;
            break;
    }
});
// function atualiza_respostas(sg_id){
//   p_id = document.querySelector("#respostas").dataset.participante
//   fetch('/diario/respostas/' + sg_id + '/' + p_id, { method: "GET"})
//   .then((response) => response.text())
//   .then((text) => {document.querySelector("#respostas").innerHTML = text;

//   })
// }