$(document).ready(function(){
    const date = new Date();
    /*De la fecha del dia en el que nos encontramos extraemos el día y el mes*/
    const dia = date.getDate();
    const mes = date.getMonth();
    $('.boton-calendario').click(function(){
        /* Estamos en el boton que no tiene id, pero el contenedor donde esta si lo tiene*/
        let idPadre = this.parentElement.id;
        let idNumero = Number(idPadre.replace("dia", ""));
        if (mes !== 11){
            $('#alerta-no-range').show();
        }

        if (dia < idNumero) {
            $('#alerta-no-range').show();
        }
        else {
            $('#pop-'+idPadre).show();
        }

    })

    $('.cerrar-regalo').click(function(){
        let Padre = this.parentElement;
        let idAbuelo = Padre.parentElement.id;
        $('#'+idAbuelo).hide();
     })

    $('#cerrar-alerta').click(function(){
        $('#alerta-no-range').hide();
    })

    $('#peligro-maray').click(function(){
        window.open('https://youtu.be/1giQVuoTAFM?si=fMMRaoHojcPuATI0&t=13');
    })

    $('#peligro-final').click(function(){
        window.open('https://youtu.be/dQw4w9WgXcQ?si=y-3IgFycDXpvyVy4&t=2');
        $('.no-regalo-texto').hide()
        $('.regalo-final').show()
    })
}
)