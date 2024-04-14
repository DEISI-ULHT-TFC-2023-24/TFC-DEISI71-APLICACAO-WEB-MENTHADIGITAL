function sleep(milliseconds) {
  const date = Date.now();
  let currentDate = null;
  do {
    currentDate = Date.now();
  } while (currentDate - date < milliseconds);
}

function atualiza_filtros(){
  const programa = document.getElementById('programa').value;
  if (programa) {    
    switch(programa){
      case 'CARE':
        document.querySelector('.filtro_care').style.display = "block";
        document.querySelector('.filtro_cog').style.display = "none";
        break;
      case 'COG':
        document.querySelector('.filtro_care').style.display = "none";
        document.querySelector('.filtro_cog').style.display = "block";
        break;
    }
  }
}

function atualiza_candidatos(){
  form_data = new FormData();
  form_data.append("programa", document.getElementById('programa').value);
  if (document.getElementById('programa').value == "CARE"){
    form_data.append("localizacao", document.getElementById('Localizações_care').value);
    form_data.append("diagnostico", document.getElementById('Diagnósticos_care').value);
    form_data.append("escolaridade", document.getElementById('Escolaridades_care').value);
    form_data.append("referenciacao", document.getElementById('Referenciações_care').value);
  }
  else if (document.getElementById('programa').value == "COG"){
    form_data.append("localizacao", document.getElementById('Localizações_cog').value);
    form_data.append("diagnostico", document.getElementById('Diagnósticos_cog').value);
    form_data.append("escolaridade", document.getElementById('Escolaridades_cog').value);
    form_data.append("referenciacao", document.getElementById('Referenciações_cog').value);
    form_data.append("gds", document.getElementById('GDS_cog').value);
  }

  csrfmiddlewaretoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
  form_data.append('csrfmiddlewaretoken',csrfmiddlewaretoken);

  fetch('/diario/obter_candidatos', {
    method: "POST",
    body: form_data,
    })
    .then(response => response.text())
    .then(document.querySelectorAll('.container-fluid').forEach((c) => {
      c.style.display = "block";
    }))
    .then(text => document.querySelector('.container-candidatos').innerHTML = text)
}

function cria_grupo(){
  lista_participantes = [];
  flag = document.getElementById('programa').value.toLowerCase();
  form_data = new FormData();
  form_data.append("programa", document.getElementById('programa').value);
  form_data.append('csrfmiddlewaretoken',document.querySelector('input[name="csrfmiddlewaretoken"]').value);
  form_data.append('nome',document.querySelector('input[name="nome"]').value);

  document.querySelectorAll('input[type="checkbox"]:checked').forEach((i) => {
    lista_participantes.push(i.value);
  });

  form_data.append('participantes',lista_participantes);

  fetch('/diario/new_group', {
    method: "POST",
    body: form_data,
    })
    .then(sleep(1500))
    .then(location.href = '/diario/?flag=' + flag)
}
