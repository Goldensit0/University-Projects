
$(document).ready(function() {
    actualizar_main();

    $('#icono_usuario').click(function() {
        $("#menu_opciones").show();
      });
});

function actualizar_main(){
    const sesion_iniciada = localStorage.getItem("sesion_iniciada");
    
    if (sesion_iniciada == "true") {
        $('#boton_inicio_sesion').hide();
        $('#boton_registrarse').hide();
        $('#icono_usuario').show();
    }
    
    //lo activamos, quitamos el inicio de sesión para que la próxima vez haya que iniciar sesión de nuevo
    //localStorage.removeItem("sesion_iniciada")
}