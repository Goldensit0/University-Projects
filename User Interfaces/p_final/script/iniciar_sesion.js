$(document).ready(function() {
    //mostrar perfil si le damos al boton
    $("#_iniciar_sesion").click(function() {
        //mostrar_datos_usuario();
        $("#popup_inicio").show();

      });
    
    //cerrar pop up si le damos a cancelar
    $("#cancelar_inicio").click(function() {
        $("#popup_inicio").hide();
    });

    $('#formulario_inicio_sesion').submit(function(event) {
        event.preventDefault();
        
        let nombre_usuario = $("#nombre_usuario").val();
        let password = $("#password").val();

        // crea/carga el array de usuarios existentes
        let usuarios_guardados = JSON.parse(localStorage.getItem("usuarios")) || [];
    
        //vamos a buscar el usuario metido en nuestro array de usuarios guardados
        let usuario_ya_existente = false;
        let contraseña_correcta = false;
        for (let i = 0; i < usuarios_guardados.length; i++){
            if (usuarios_guardados[i].nombre_usuario == nombre_usuario){
                usuario_ya_existente = true;
                //tienen que coincidir tanto el usuario como la contraseña
                if (usuarios_guardados[i].password == password){
                contraseña_correcta = true;
                }
            }
        }
        
        //ahora condicionales para los posibles casos:
        if (!usuario_ya_existente){
        alert("Usuario no existente. Por favor, regístrese en la web.");
        } else if(usuario_ya_existente && !contraseña_correcta){
        alert("Contraseña incorrecta");
        }
        else{
        
            localStorage.setItem("sesion_iniciada", "true");
            localStorage.setItem("usuario_iniciado", nombre_usuario);
            //añado el usuario, nos servirá para poder editar el perfil más tarde
            //alert("Sesión iniciada correctamente")
            $("#popup_inicio").hide();
            //recargar pagina
            window.location.href = 'main.html';
        }
    });
});