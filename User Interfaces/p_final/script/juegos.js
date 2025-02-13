$(document).ready(function () {
    // este archivo cargará los juegos de la sección "Juega"
    showCarga();

    let container =  $('.juegos');
    let circulito = $('#target-juego-1');
    let bolita = $('#target-juego-2');
    let barra = $('.barra-juego2');

    let tiempoJuegos = $(".tiempo-texto");
    let puntosJuegos = $(".score-texto");

    // Cogemos la posición de nuestro container para sumarla a los cálculos
    let posXContainer = container.position().left;
    let posYContainer = container.position().top;

    tiempoJuegos.hide();
    puntosJuegos.hide();
    circulito.hide();
    bolita.hide();
    barra.hide();

    function defaultBack(){
        // Esta funcion hace que volvemos al estado default en todos los juegos:
        // cero puntos y un minuto y medio de valor de tiempo restante
        puntosJuegos.text(0);
        tiempoJuegos.text(1 + ":" + 30);

        // Escondemos los puntos y el tiempo
        puntosJuegos.hide();
        tiempoJuegos.hide();
    }
    function defaultBack1(){
        circulito.hide();
    }
    function defaultBack2(){
        bolita.hide();
        barra.hide();
    }
    function showOver(){
        $('.juego1').hide();
        $('.juego2').hide();
        $('.game-over').show();
    }
    function showCarga(){
        $('.juego1').hide();
        $('.juego2').hide();
        $('.game-over').hide();
        $('.pantalla-carga').show();

    }
    function showJuego1(){
        $('.juego1').show();
        $('.juego2').hide();
        $('.game-over').hide();
        $('.pantalla-carga').hide();
        circulito.show();
        puntosJuegos.show();
        tiempoJuegos.show();
        bolita.hide();
        barra.hide();
        defaultBack();
    }
    function showJuego2(){
        $('.juego1').hide();
        $('.juego2').show();
        $('.game-over').hide();
        $('.pantalla-carga').hide();
        bolita.show();
        barra.show();
        circulito.hide();
        puntosJuegos.show();
        tiempoJuegos.show();
        defaultBack();
    }

    function moverCirculito(){
        // esta funcion mueve aleatoriamente el objeto del "puffle"
        circulito.show();

        // Definimos el área localizada donde el circulito puede aparecer
        let anchoContainer = container.width();
        let altoContainer = container.height();
        let anchoCirculito = circulito.width();
        let altoCirculito = circulito.height();

        // Calculamos la posición random dentro de ese rango
        let posX = Math.random() * (anchoContainer - anchoCirculito) + posXContainer;
        let posY = Math.random() * (altoContainer - altoCirculito) + posYContainer;

        // La colocamos donde toca
        circulito.css({
            left: posX + 'px',
            top: posY + 'px'
        });
    }

    function moverBarra(derechaPresionado, izquierdaPresionado, posBarraX){
        // esta funcion hace que podamos mover la barrita (pinguino) al presionar las flechas izq y der
        let anchoContainer = container.width();
        let anchoBarra = barra.width();

        if (derechaPresionado && posBarraX < anchoContainer - anchoBarra) {
            posBarraX += 7;
        }
        else if (izquierdaPresionado && posBarraX > 0) {
            posBarraX -= 7;
        }
        // La colocamos donde toca
        barra.css({
            left: posBarraX + 'px',
        });
        return posBarraX;
    }

    // JUEGO 1: ATRAPAME SI PUEDES: PINCHAR EN EL PUFFLE LA MAYOR CANTIDAD DE VECES EN UN TIEMPO DADO
    $("#boton-juego-1").on("click", function juego1() {
        // Escondemos la pantalla de carga y sacamos el juego que sí es
        showJuego1();

        // Inicializamos los puntos
        let puntos = 0;

        // Ahora el juego:
        moverCirculito(); // LLamamos a la funcion que mueve el puffle
        let tiempo = 90; // Un minuto 30 en segundos

        // Actualizamos el timer
        let cuentaAtras = setInterval(function () {
            // cada segundo restaremos 1 a nuestra cuenta atrás
            tiempo--;

            let mins = Math.floor(tiempo / 60);
            let secs = Math.floor(tiempo % 60);

            // Actualizamos los valores
            $(".tiempo-texto").text(mins + ":" + secs);

            if (tiempo <= 0) {
                defaultBack();  // Esta función vuelve a la página inicial porque se ha acabado el tiempo
                defaultBack1();
                showOver();
                clearInterval(cuentaAtras);
            }
            $("#boton-reinicio-juego").on("click", function() {
                defaultBack();
                defaultBack1();
                showCarga();
                clearInterval(cuentaAtras);

            })
        }, 1000);

        circulito.on("click", function(){
            circulito.attr('src', 'images/ojo-cerrado.png');
            setTimeout(() => {
                circulito.attr('src', 'images/ojo-abierto.png');
            }, 300); // 1000 ms = 1 segundo

            moverCirculito();
            // sumamos puntos al contador
            puntos++;
            $(".score-texto").text(puntos);
        });
    });


    // JUEGO 2 -- Bolita lanzadera será un juego tipo "pong" en el que, cada vez que la bolita
    // toque el techo, sumamos un punto. Si la bolita se pierde por abajo, game over :(
    $("#boton-juego-2").on("click", function juego2() {
        showJuego2();

        // cada vez que pulsemos las flechas izquierda o derecha, moveremos la barra (el pinguino)
        let derechaPresionado = false;
        let izquierdaPresionado = false;

        // definimos las posiciones de la barra que movemos nosotros(pingüino)
        let posBarraX = container.width()/2 - barra.width();
        let posBarraY = posYContainer - container.height() + barra.height() - 10;
        // colocamos al pingüino centradito y abajo
        barra.css({
            left: posBarraX + 'px',
            top: posBarraY + 'px'
        });

        // estas funciones definen que el pingüino se mueva cuando pulsemos "a", "d" o las flechas
        $(document).on("keydown", function (e) {
            if (e.key === "ArrowRight") derechaPresionado = true;
            if (e.key === "d") derechaPresionado = true;
            if (e.key === "ArrowLeft") izquierdaPresionado = true;
            if (e.key === "a") izquierdaPresionado = true;
        });

        $(document).on("keyup", function (e) {
            if (e.key === "ArrowRight") derechaPresionado = false;
            if (e.key === "d") derechaPresionado = false;
            if (e.key === "ArrowLeft") izquierdaPresionado = false;
            if (e.key === "a") izquierdaPresionado = false;
        });

        // valores iniciales de la bolita
        let posXBolita = posBarraX;
        let posYBolita = posYContainer-container.height();
        bolita.css({
            left: posXBolita + "px",
            top: posYBolita + "px"
        });

        // variables de velocidad
        let velocidadBolitaX = 4;
        let velocidadBolitaY = 4;

        // bucle del juego, recarga cada 16 ms
        const intervaloJuego = setInterval(function () {
            bolita.show();
            // cambiamos los valores de la posicion de la barra con la funcion de moverla
            posBarraX = moverBarra(derechaPresionado, izquierdaPresionado, posBarraX);

            // va a moverse la pelotita a 60 fps (timeout de 16 ms)
            let anchoContainer = container.width();
            let altoContainer = container.height();

            // chequeamos colisiones con paredes
            /*
            if (posYBolita <= posYContainer){
                velocidadBolitaY = -velocidadBolitaY;
            }
            if(posXBolita >= posXContainer+anchoContainer){
                velocidadBolitaX = -velocidadBolitaX;
            }
            if (posXBolita <= posXContainer){
                velocidadBolitaX = -velocidadBolitaX;
            }
            if (posYBolita > posYContainer+altoContainer){
                // Hemos llegado al suelo, game over
                showOver();
                defaultBack2();
                clearInterval(intervaloJuego);
            }*/
            // Rebotar en paredes, el techo y la barra
            if (posXBolita + bolita.width() > anchoContainer || posXBolita < 0) {
                velocidadBolitaX = -velocidadBolitaX;
            }
            if (posYBolita < 0) {
                velocidadBolitaY = -velocidadBolitaY;
                puntosJuegos++;
            }
            if (
                posYBolita + bolita.width() >= posBarraY &&
                posXBolita + bolita.width() >= posBarraX &&
                posXBolita <= posBarraX + barra.width()
            ) {
                velocidadBolitaY = -velocidadBolitaY;
            }

            if (posYBolita > altoContainer) {
                // Hemos llegado al suelo, game over. Paramos el bucle
                showOver();
                defaultBack2();
                clearInterval(intervaloJuego);
            }


            // chequeamos colisiones con el pinguino
            if((posYBolita === posBarraY) && (posBarraX <= posXBolita <= posBarraX+barra.width())){
                velocidadBolitaY = -velocidadBolitaY;
                // aleatoriamente, cambiará la dirección en la que se mueve la bola en el eje x
                function rand(min, max){
                    return Math.floor(Math.random() * (max - min)) + min;
                }
                if (rand(1,2) === 1){
                    velocidadBolitaX = -velocidadBolitaX;
                }
            }

            // movimiento de bolita
            if(velocidadBolitaY>0){
                posYBolita -= velocidadBolitaY;
            }
            if(velocidadBolitaY<0){
                posYBolita += velocidadBolitaY;
            }
            if(velocidadBolitaX>0){
                posXBolita -= velocidadBolitaX;
            }
            if(velocidadBolitaX<0){
                posXBolita += velocidadBolitaX;
            }

            // actualizamos las posiciones del css
            bolita.css({
                left: posXBolita + "px",
                top: posYBolita + "px"
            });

            $("#boton-reinicio-juego").on("click", function(){
                showCarga();
                defaultBack2();
                clearInterval(intervaloJuego);
            })
            $("#boton-juego-1").on("click", function(){
                defaultBack2();
                clearInterval(intervaloJuego);
            })

        }, 16);

        /*
        // posición inicial de la bolita
        let posBolitaX = posBarraX;
        let posBolitaY = posBarraY;
        // Bucle principal, se va a ir recargando todo el rato
        const intervaloJuego = setInterval(function () {
            let resultadoBolita = moverBolita(posBolitaX, posBolitaY, velocidadBolitaX, velocidadBolitaY, posBarraX, posBarraY);
            posBolitaX = resultadoBolita.posX;
            posBolitaY = resultadoBolita.posY;
            velocidadBolitaX = resultadoBolita.velX;
            velocidadBolitaY = resultadoBolita.velY;
            posBarraX = moverBarra(derechaPresionado, izquierdaPresionado, posBarraX);
            // Actualizo su posicion
            bolita.css({
                left: posBolitaX + "px",
                top: posBolitaY + "px"
            });
            // Actualizamos los valores
            $(".tiempo-texto").text(mins + ":" + secs);

            $("#boton-reinicio-juego").on("click", function() {
                clearInterval(intervaloJuego);
                showCarga()
                defaultBack2();
                defaultBack();
            })

        }, 16); // 60 fps

        function moverBolita(posBolitaX, posBolitaY, velocidadBolitaX, velocidadBolitaY, posBarraX, posBarraY){
            let anchoContainer = container.width();
            let altoContainer = container.height();
            let anchoBolita = bolita.width();
            let anchoBarra = barra.width();

            posBolitaX += velocidadBolitaX;
            posBolitaY += velocidadBolitaY;
            // Rebotar en paredes, el techo y la barra
            if (posBolitaX + anchoBolita > anchoContainer || posBolitaX < 0) {
                velocidadBolitaX = -velocidadBolitaX;
            }
            if (posBolitaY < 0) {
                velocidadBolitaY = -velocidadBolitaY;
                puntosJuegos++;
            }
            if (
                posBolitaY + anchoBolita >= posBarraY &&
                posBolitaX + anchoBolita >= posBarraX &&
                posBolitaX <= posBarraX + anchoBarra
            ) {
                velocidadBolitaY = -velocidadBolitaY;
            }

            // Si toca el suelo paramos el bucle
            if (posBolitaY > altoContainer) {
                clearInterval(intervaloJuego);
                showOver();
                return { posX: posBolitaX, posY: posBolitaY, velX: velocidadBolitaX, velY: velocidadBolitaY };
            }

            return { posX: posBolitaX, posY: posBolitaY, velX: velocidadBolitaX, velY: velocidadBolitaY };
        }*/

    })
});

