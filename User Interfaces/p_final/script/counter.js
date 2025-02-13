
// Con esta primera función chequearemos que el documento esté listo antes de ejecutar ninguna otra cosa
$(document).ready(function(){

    // CONTADOR: --------------------------------------------------------------------------------------------
    const fechaNavidad = new Date('Dec 25, 2024 00:00:00').getTime();

    // hacemos que se refresque cada segundo con la función set interval
    let counter = setInterval(function() {
            const fechaActual = new Date().getTime();
            let diferencia = fechaNavidad - fechaActual;

            switch(true) {
                case(diferencia > 0):
                    //Como Date usa de referencia el 1 de enero de 1970 y lo hace en milisegundos,
                    //tenemos que hacer ciertos cálculos. Los pasaremos a números enteros con parseInt

                    let dias = parseInt(diferencia / (1000 * 60 * 60 * 24), 10);
                    let horas = parseInt((diferencia % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60), 10);
                    let mins = parseInt((diferencia % (1000 * 60 * 60)) / (1000 * 60), 10);
                    let secs = parseInt((diferencia % (1000 * 60)) / 1000, 10)

                    //ponemos esos valores en nuestras clases correspondientes de html
                    $('.dias').text(dias);
                    $('.horas').text(horas);
                    $('.minutos').text(mins);
                    $('.segundos').text(secs);

                    break;

                case (diferencia <= 0):
                    //limpiamos el intervalo para parar de refrescar
                    clearInterval(counter);

                    //ponemos que quedan 0 minutos, horas, dias y segundos
                    $('.dias, .horas, .minutos, .segundos').text("00");

                    break;

            }
        }, 1000  // al estar en milisegundos queremos que se refresque cada 1000
    )

})