$(document).ready(function() {

    //array con los vídeos que saldrán aleatoriamente
    const videos = [
        "https://www.youtube.com/embed/XBS2Qv8ZMa4?autoplay=1&controls=0&autohide=1&modestbranding=1&showinfo=0", //papas noeles
        "https://www.youtube.com/embed/C351jKJmLTo?autoplay=1&controls=0&autohide=1&modestbranding=1&showinfo=0", //baltasa el patinete
        "https://www.youtube.com/embed/tulDL5btdYw?autoplay=1&controls=0&autohide=1&modestbranding=1&showinfo=0", //renos
        "https://www.youtube.com/embed/fAcVS-CdTz4?autoplay=1&controls=0&autohide=1&modestbranding=1&showinfo=0", // papa noel corriendo
        "https://www.youtube.com/embed/4QWRg-IS50o?autoplay=1&controls=0&autohide=1&modestbranding=1&showinfo=0"  // last crhistmas
    ];

    let video_repro = null; //video reproduciendose en este momento

    //mostrar popup videollamada si le damos al boton
    $("#videollamada").click(function() {
        $("#popup_videollamada").show();
      });

    //cerrar pop up si le damos a salir
    $("#salir").click(function() {
        stop_video(); //si hubiera algún vídeo en marcha
        $("#popup_videollamada").hide();
    });

    $('#llamar').click(function () {
        stop_video(); // Detener el video anterior si hay uno
        cargando(); //le ponemos pantallita de carga de 2 segundines

        setTimeout(() => {
            cerrar_cargando();
            random_video();
        }, 2000); // Simula pantalla de carga de 2 segundos
    });

    // colgar --> cierra el video
    $('#colgar').click(function () {
        stop_video();
    });

    function cargando() {
        $('.container_video').hide();
        $('.pantalla_carga').show();
    }

    function cerrar_cargando() {
        $('.pantalla_carga').hide();
        $('.container_video').show();
    }

    function random_video() {
        const randomIndex = Math.floor(Math.random() * videos.length); 
        video_repro = videos[randomIndex]; //elegimos numero random de enttre nuestras opciones
        $('#video').attr('src', video_repro);
    }

    function stop_video() {
        $('#video').attr('src', ''); // Quita el video actual
        $('.container_video').hide();
    }
});

