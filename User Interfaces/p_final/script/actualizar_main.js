$(document).ready(function() {
    actualizar_main();

    $('#icono_usuario').click(function() {
        $("#desplegable_usuario").toggle();
      });

});


function actualizar_main(){
    const sesion_iniciada = localStorage.getItem("sesion_iniciada");
    if (sesion_iniciada === "true") {
        $('#registrarse').hide();
        $('#_iniciar_sesion').hide();
        //$('#icono_usuario').show();
        //-------------------MOVER DE SITIO ESTE BOTON PARA QUE NO INTERFIERA CON LA öLèvª
        $("#cerrar_sesion").show();
        $("#editar_perfil").show();
        $("#historial_compra").show();
        $("#videollamada").show();
        $("#mis_cartas").show();

        //mostramos el icono con una foto de perfil (cambiamos la clase del botón a la de un usuario loggeado)
        $("#icono_usuario").removeClass("icono_invitado").addClass("icono_sesion_iniciada");
    }
}