console.log("jquery.js loaded");
$(document).ready(function () {
        section = "participants"
        history.pushState({section: section}, "", ``);
        history.pushState({section: section}, "", ``);
        window.onpopstate = function (event) {
            if (event.state != null) {
                showSection(event.state.section);
            }
        }

        function submitForm() {
            var radios = document.querySelectorAll('input[type="radio"]');
            var isChecked = false;

            for (var i = 0; i < radios.length; i++) {
                if (radios[i].checked) {
                    isChecked = true;
                    break;
                }
            }

            if (!isChecked && radios.length > 0 ) {
                alert('Por favor, preencha o formulário');
                return false; // Prevent form submission
            }

            return true; // Allow form submission
        }

        function showSection(section) {
            $.ajax({
                method: 'GET',
                url: section,
                success: function (data) {
                    $('.page-content').html(data);

                    if (document.querySelector('#id_time')) {

                        var today = new Date();
                        var currentTime = today.getHours() + ":" + today.getMinutes();
                        var year = today.getFullYear();
                        var month = (today.getMonth() + 1).toString().padStart(2, '0');
                        var day = today.getDate().toString().padStart(2, '0');
                        var currentDate = year + "-" + month + "-" + day;

                        document.querySelector('#id_time').value = currentTime;
                        document.querySelector('#id_data').value = currentDate;

                    }

                    if (seconds > 0 || ticking) {
                        seconds = 0;
                        ticking = false;
                    }
                    NProgress.done(true);
                },
                error: function () {
                    console.log("Error!");
                    alert("Pagina não disponível.");
                }
            });
        }

        showSection(section)

        $(document).on("click", ".jq-btn", function () {
            NProgress.start()
            element = $(this)
            var href = element.attr("data-href").replace('#', '');
            var section = ""


            if (href == "dashboard") {
                section = "dashboard-content";
            } else {
                section = href;
            }

            history.pushState({section: section}, "", ``);
            showSection(section)
            if (element.hasClass('nav-link')) {
                $(".nav-link").removeClass("active");
            }
        });

        var seconds = 0;
        var ticking = false;

        function tick() {
            if (ticking) {
                var counter = document.getElementById("clock");
                seconds++;
                counter.innerHTML =
                    "0:" + (seconds < 10 ? "0" : "") + String(seconds);
                if (seconds < 60) {
                    setTimeout(tick, 1000);
                } else {
                    document.getElementById("clock").innerHTML = "1:00";
                }
            }
        }

        $(document).on("click", ".btn-timer", function () {
            ico = $('#timer-ico');
            if (ico.hasClass('fa-pause')) {
                ico.removeClass('fa-pause');
                ico.addClass('fa-play');
            } else {
                ico.addClass('fa-pause');
                ico.removeClass('fa-play');
            }
            ticking = (ticking == true) ? false : true
            tick();
        })


        $(document).on("click", ".delete-same-id", function () {
            id = this.id;
            id = id.replace(/\s/g, '');
            console.log(id)
            var list = document.querySelectorAll('#collapse' + $.trim(id))

            for (i = 0; i < list.length; i++) {
                if (i >= 1) {
                    list[i].remove();
                }
            }
        })

        $(document).on("click", ".toggle", function () {
            console.log("on toggle")
            console.log($(this).id)
            e = $(document).getElementsByClassName($(this).id)
            e.toggle();

        });

        $(document).on("click", ".btn-submit", function (event) {
            event.preventDefault();
            if (submitForm()) {
                var href = $(this).attr("data-href");
                const csrf_token = Cookies.get('csrftoken');
                var post_data = $("#question-form").serialize();

                $.ajax({
                    method: 'POST',
                    url: href,
                    data: post_data,
                    headers: {'X-CSRFToken': csrf_token},
                    async: false,
                    success: function (data) {
                        console.log("Success!");
                        $('.page-content').html(data);
                    },
                    error: function () {
                        console.log("Error!");
                        alert("Página não disponível.");
                    }
                });
            }
        });

        $(document).on("click", ".btn-update-profile", function (event) {
            event.preventDefault();
                var href = $(this).attr("data-href");
                const csrf_token = Cookies.get('csrftoken');
                var post_data = $("#update-form").serialize();

                $.ajax({
                    method: 'POST',
                    url: href,
                    data: post_data,
                    headers: {'X-CSRFToken': csrf_token},
                    async: false,
                    success: function (data) {
                        console.log("Success!");
                        $('.page-content').html(data);
                    },
                    error: function () {
                        console.log("Error!");
                        alert("Página não disponível.");
                    }
                });
        });

        $(document).on("click", ".btn-appointment", function () {
            event.preventDefault();
            var href = $(this).attr("data-href");
            console.log("href:", href)
            const csrf_token = Cookies.get('csrftoken');
            var form_data = new FormData();
            form_data.append('part', document.getElementById("id_part").value)
            form_data.append('data', document.getElementById("id_data").value)
            form_data.append('time', document.getElementById("id_time").value)

            $.ajax({
                method: 'POST',
                url: href,
                data: form_data,
                headers: {'X-CSRFToken': csrf_token},
                async: false,
                processData: false,
                contentType: false,
                success: function (data) {
                    console.log("Success!")
                    console.log($('.page-content'))
                    $('.page-content').html(data);
                    return false;
                },
                error: function () {
                    console.log("Error!");
                    alert("Pagina não disponível.");
                }
            })
        });


        $(document).on("click", ".btn-registar", function () {
            event.preventDefault();
            console.log('registar');
            var href = $(this).attr("data-href");
            const csrf_token = Cookies.get('csrftoken');
            var post_data = $("#patient-form").serialize();
            console.log(post_data);
            const f = document.getElementById('patient-form');
            var problem = false;
            Object.values(f).forEach((val) => {
                if (val.type != 'submit' && val.value == '') {
                    problem = true;
                }
            });

            if (problem) {
                alert('Deve preencher todos os campos do formulário')
            } else {
                $.ajax({
                    method: 'POST',
                    url: href,
                    data: post_data,
                    headers: {'X-CSRFToken': csrf_token},
                    async: false,
                    success: function (data) {
                        console.log("Success!")
                        $('.page-content').html(data);
                        return false;
                    },
                    error: function () {
                        console.log("Error!");
                        alert("Pagina não disponível.");
                    }
                })
            }
        });

        $(document).on("click", ".btn-submit-upl", function () {
            event.preventDefault();
            var form = $("#upl-form");
            var form_data = new FormData(form[0]);
            var href = $(this).attr("data-href");
            const csrf_token = Cookies.get('csrftoken');

            console.log(form_data);
            $.ajax({
                method: 'POST',
                url: href,
                data: form_data,
                mimeType: "multipart/form-data",
                headers: {'X-CSRFToken': csrf_token},
                contentType: false,
                processData: false,
                async: false,
                success: function (data) {
                    console.log("Success!")
                    $('.page-content').html(data);
                    return false;
                },
                error: function () {
                    console.log("Error!");
                    alert("Pagina não disponível.");
                }
            })
        });

        $(document).on("click", ".jq-report-btn", function () {
            console.log();
            $.ajax({
                method: 'POST',
                url: href,
                data: form_data,
                mimeType: "multipart/form-data",
                headers: {'X-CSRFToken': csrf_token},
                contentType: false,
                processData: false,
                async: false,
                success: function (data) {
                    console.log("Success!")
                    $('.container').html(data);
                    return false;
                },
                error: function () {
                    console.log("Error!");
                    alert("Pagina não disponível.");
                }
            })
        });
        //quero fazer uma jquery ou função que quando carrego no botão de adicionar uma nova linha, ele vai buscar o valor do input e adiciona a uma nova linha na tabela com o valor do input
    }
)

