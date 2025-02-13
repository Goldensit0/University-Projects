const contenedor = document.getElementById("col_juegos");
const objetivo = document.getElementById("objetivo_juego");
const caja_puntuacion = document.getElementById("juego1_caja");
interval = null; // Inicializa el contador
hit = new Audio('audio/hit.mp3'); // Sonido al hacer click en el objetivo

let tiempo = 90; // Tiempo en segundos
let puntuacion = 0; // Puntuación inicial

function reiniciar_valores() {
    tiempo = 90;
    puntuacion = 0; // Reinicia los valores originales
    document.getElementById("tiempo").innerHTML = tiempo;
    document.getElementById("puntuacion").innerHTML = puntuacion;
}

function actualizar_tiempo() {
    tiempo--;
    document.getElementById("tiempo").innerHTML = tiempo;
}

function actualizar_puntuacion() {
    puntuacion++;
    document.getElementById("puntuacion").innerHTML = puntuacion;
}

function moverObjetivo() {

    // Calcular las dimensiones del contenedor y la imagen
    const contenedorWidth = contenedor.clientWidth *0.95;
    const contenedorHeight = contenedor.clientHeight *0.95;
    const objetivoWidth = objetivo.clientWidth;
    const objetivoHeight = objetivo.clientHeight;

    // Calcular posiciones aleatorias dentro del contenedor
    const maxX = (contenedorWidth - objetivoWidth) * 0.9; // Para que no se salga de la pantalla
    const maxY = (contenedorHeight - objetivoHeight) * 0.95; // Para que no se salga de la pantalla
    let nuevaX = Math.floor(Math.random() * maxX);
    let nuevaY = Math.floor(Math.random() * maxY);

    if (nuevaX < (0.10 * maxX)) { // Para que no se salga por la izquierda
        nuevaX = 0.10 * maxX;
    }
    if (nuevaY < (0.10 * maxY)) { // Para que no se salga por arriba
        nuevaY = 0.10 * maxY;
    }

    // Aplicar las nuevas posiciones a la imagen
    objetivo.style.left = `${nuevaX}px`;
    objetivo.style.top = `${nuevaY}px`;

    // Reproducir sonido
    hit.play();

    // Aumentar la puntuación
    actualizar_puntuacion();

}

function tiempo_restante(){
    if (tiempo <= 0) { // Fin del juego
        objetivo.style.display = 'none';
        caja_puntuacion.style.top = Math.floor(contenedor.clientHeight/2) + "px"; // Mover al medio
        clearInterval(interval); // Detiene el contador
    }
    else { // Actualiza el tiempo
        actualizar_tiempo();
    }
}