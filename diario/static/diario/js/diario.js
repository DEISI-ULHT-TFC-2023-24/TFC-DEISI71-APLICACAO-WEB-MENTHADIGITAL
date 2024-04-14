function toggleChevron(id) {
    element = document.getElementById(id);

    if (element.classList.contains('fa-chevron-left')) {
        element.classList.remove('fa-chevron-left');
        element.classList.add('fa-chevron-right');
    } else {
        element.classList.add('fa-chevron-left');
        element.classList.remove('fa-chevron-right');
    }
}

function toggleVideoconf() {
    element = document.getElementById("videoconf");
    content = document.getElementById("content");

    if (content.style.gridTemplateRows == "0px 1fr") {
        content.style.gridTemplateRows = "100px 1fr"
        element.style.height = "100px";
    } else {
        content.style.gridTemplateRows = "0px 1fr"
        element.style.height = "0px";
    }
}


function moveSidebar() {
    element = document.getElementById("sidebar");
    content = document.getElementById("content");
    diario = document.getElementById("diario");

    //esconder sidebar
    if (element.style.width === "250px") {
        element.style.width = "82px";
        content.style.marginLeft = "87px";
        content.style.width = `calc(100% - 87px)`;

        document.querySelectorAll('.sidebar-text').forEach(function (e) {
            e.style.display = "none";
        });

        document.getElementById('container-logo').style.alignItems = "flex-start";
        document.getElementById('logo').style.display = "none";


        //mostrar sidebar
    } else {
        element.style.width = "250px";
        content.style.marginLeft = "250px";
        content.style.width = `calc(100% - 250px)`;

        document.querySelectorAll('.sidebar-text').forEach(function (e) {
            e.style.display = "inline-block";
        });

        document.getElementById('container-logo').style.alignItems = "center";
        document.getElementById('logo').style.display = "block";
    }
}

function moveDiario() {
    element = document.getElementById("diario");
    content = document.getElementById("content");
    icon = document.getElementById("btn-diario");
    var width = (window.innerWidth > 0) ? window.innerWidth : screen.width;
    //esconder sidebar

    if (content.style.gridTemplateColumns != "1fr 0fr") {
        content.style.gridTemplateColumns = "1fr 0fr";

        icon.classList.remove("fa-xmark");
        icon.classList.add("fa-book-bookmark");
        document.querySelectorAll(".bcca-breadcrumb-item span").forEach(it => {
            it.style.display = "inline";
        })
        document.querySelectorAll(".bcca-breadcrumb-item-last span").forEach(it => {
            it.style.display = "inline";
        })


        //mostrar sidebar
    } else {
        content.style.gridTemplateColumns = "1fr 0.5fr";
        icon.classList.add("fa-xmark");
        icon.classList.remove("fa-book-bookmark");
        document.querySelectorAll(".bcca-breadcrumb-item span").forEach(it => {
            it.style.display = "none";
        })
        document.querySelectorAll(".bcca-breadcrumb-item-last span").forEach(it => {
            it.style.display = "none";
        })
    }
}

window.addEventListener("DOMContentLoaded", (event) => {
    //inicializar valores para as funcoes de toggle funcionarem
    document.getElementById("videoconf").style.height = "0px";
    document.getElementById("sidebar").style.width = "82px";
    document.getElementById("content").style.gridTemplateColumns = "1fr 0fr";
    document.getElementById("content").style.gridTemplateRows = "0px 1fr";
});


$(document).on("click", ".sidebar-toggle-btn", function () {
    moveSidebar();
    toggleChevron('sidebar-icon');
});

$(document).on("click", ".videoconf-button", function () {
    toggleVideoconf();
});

$(document).on("click", ".diario-toggle-btn", function () {
    moveDiario();
    toggleChevron('btn-diario')
});


const adjustLayout = () => {
    const width = window.innerWidth > 0 ? window.innerWidth : screen.width;
    const breadcrumbItems = document.querySelectorAll(".bcca-breadcrumb-item span");
    const breadcrumbLastItems = document.querySelectorAll(".bcca-breadcrumb-item-last span");
    const contentElement = document.querySelector("#content");
    const diarioElement = document.querySelector("#diario");
  
    if (width > 1300) {
      breadcrumbItems.forEach(it => {
        it.style.display = "inline";
      });
      breadcrumbLastItems.forEach(it => {
        it.style.display = "inline";
      });
    } else {
      breadcrumbItems.forEach(it => {
        it.style.display = "none";
      });
      breadcrumbLastItems.forEach(it => {
        it.style.display = "none";
      });
    }
  
        if (width > 1400) {
      contentElement.style.display = "grid";
      contentElement.style.gridTemplateColumns = "1fr 0fr";
      contentElement.style.gridTemplateRows = "0px 1fr";
      contentElement.style.gridTemplateAreas = "'video video''main aside'";
      contentElement.style.width = "100%";
      contentElement.style.marginLeft = "87px";
      diarioElement.style.height = "100vh";
    } else {
      contentElement.style.display = "grid";
      contentElement.style.gridTemplateColumns = "1fr";
      contentElement.style.gridTemplateRows = "0px auto auto";
      contentElement.style.gridTemplateAreas = "'video''main''aside'";
      contentElement.style.width = "100%";
      contentElement.style.marginLeft = "87px";
      diarioElement.style.height = "inherit";
    }
    
  };
  
  window.addEventListener("resize", adjustLayout);
  window.addEventListener("DOMContentLoaded", adjustLayout);
