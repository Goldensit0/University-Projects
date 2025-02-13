$(document).ready(function() {
    //mostrar perfil si le damos al boton
    $("#registrarse").click(function() {
        //mostrar_datos_usuario();
        $("#popup_registro").show();

    });
    
    

    $('#formulario_registro').submit(function(event) {
        event.preventDefault();

        //cargamos los valores introducidos
        let nombre_usuario = $("#nombre_usuario_new").val();
        let password = $("#password_new").val();
        let password_repe=$("#password_repe").val();
        let correo = $("#correo_new").val();
        let ciudad = $("#ciudad_new").val();
        let genero = $("#genero_new").val();

        //VALIDAMOS
        //restricciones de la contraseña
        const nums = (password.match(/[0-9]/g) || []).length; //tamaño del array que contiene todos los números metidos en la contraseña
        const mayus = /[A-Z]/.test(password); //booleano, true si detecta alguna mayúscula
        const minus = /[a-z]/.test(password); //booleano, para minúsculas
        const especiales = /[_@.%]/.test(password); //consideraremos especiales _ . @ y %

        let input_no_validos = true;
        //lo hacemos con else if para que no salten todas las alertas de golpe si hubiera varias
        //NOTA: el correo se valida directamente en el .html
        if (nombre_usuario.length < 3) {
            alert("Nombre mínimo 3 caracteres");
            input_no_validos = false;
            } else if (password.length != 12 || nums < 2 || mayus==false || minus==false || especiales==false){
            alert("La contraseña debe contener 12 caracteres y al menos dos números, una mayúscula, una minúscula y un caracter especial (_ . @ %)");
            input_no_validos = false;
            } else if (password != password_repe){
            alert("Las contraseñas no coinciden")
            input_no_validos = false;
            } else if (ciudad.length < 3) {
            alert("Ciudad mínimo 3 caracteres");
            input_no_validos = false;
        }

        //si lelgamos aquí todos los datos eran correctos, creamos al usuario
        if (input_no_validos){
            var usuario_datos = {
                nombre_usuario: nombre_usuario,
                password: password,
                correo: correo,
                ciudad: ciudad,
                genero:genero
            };

            //crea/carga el array
            let usuarios_guardados = JSON.parse(localStorage.getItem('usuarios')) || [];

            //vamos a buscar el usuario metido en nuestro array de usuarios guardados
            let usuario_ya_existente = false;
            
            for (let i = 0; i < usuarios_guardados.length; i++){
                if (usuarios_guardados[i].nombre_usuario == nombre_usuario){
                usuario_ya_existente = true;
                }
            }
            
            if (!usuario_ya_existente){
                usuarios_guardados.push(usuario_datos);
                // guardar en local storage
                localStorage.setItem("usuarios", JSON.stringify(usuarios_guardados));
                alert("Usuario registrado :)");
                $("#popup_registro").hide(); //cerramos popup
            }

            else if (usuario_ya_existente){
                alert("Este usuario ya está registrado");
            }
        }
        
    });

    //cerrar pop up si le damos a cancelar
    $("#cancelar_registro").click(function() {
        if (confirm("¿Estás seguro de que deseas cancelar? Todos los cambios se perderán.")) {
            $("#popup_registro").hide();
        }
    });

    // boton limpiar
    $("#limpiar_formulario").click(function() {
        if (confirm("¿Borrar datos?")) {
            $("#formulario_registro")[0].reset();
        }
    });

});