$(document).ready(function() {
    //mostrar cerrar sesion si le damos al boton
    $("#b_cerrar_sesion").click(function() {
        $("#popup_cerrar_sesion").show();
      });

    
    //cerrar pop up si le damos a cancelar
    $("#cancelar_cerrar_sesion").click(function() {
        $("#popup_cerrar_sesion").hide();
    });

    // confirmacion cierre de sesion
    $("#confirmar_cerrar_sesion").click(function() {
        $("#popup_cerrar_sesion").hide();
        
        //Quitamos la constante que mantiene la sesión iniciada
        localStorage.getItem("sesion_iniciada");
        localStorage.removeItem("sesion_iniciada");
        //borro el nombre del usuario iniciado tambien
        localStorage.getItem("usuario_iniciado");
        localStorage.removeItem("usuario_iniciado");
        location.reload();
    });
});