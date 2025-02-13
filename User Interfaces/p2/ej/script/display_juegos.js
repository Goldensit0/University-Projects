function ocultar_todo() {
    const images = document.querySelectorAll('.imagen_juego');
    images.forEach(image => {
      image.style.display = 'none';
    });
    document.getElementById("objetivo_juego").style.display = 'none';
    const caja = document.getElementById("juego1_caja");
    caja.style.display = 'none';
    caja.style.top = 0; // Devolver a arriba
    document.getElementById("col_juegos").style.backgroundColor = "#66abeb";

    // Detiene el contador si estaba corriendo
    if (interval){clearInterval(interval);}
}


function show_juego1(imageID) { // Boton de juego 1
  document.getElementById(imageID).style.display = "block";
  reiniciar_valores(); // Reinicia los valores
  objetivo.style.display = 'block'; // Muestra el objetivo
  caja_puntuacion.style.display = 'flex'; // Muestra la caja de puntuación
  objetivo.addEventListener("click", moverObjetivo); // Inicia el rastreo de clicks al objetivo
  interval = setInterval(tiempo_restante, 1000); // Actualizar cada segundo
}

function show_juego2(imageID) { // Boton de juego 2
  document.getElementById(imageID).style.display = "block";
  resetGame();
}

function showImage(imageId) {
    ocultar_todo();
  
    // Muestra la imagen seleccionada
    if (imageId === 'imagen1') {
      console.log("Juego 1");
      show_juego1(imageId);
    }
    else if (imageId === 'imagen2') {
      show_juego2(imageId);
    }
    else {
    const selectedImage = document.getElementById(imageId).style.display = 'block';
    }
}