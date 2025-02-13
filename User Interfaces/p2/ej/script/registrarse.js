$(document).ready(function() {
    //REGISTRARSE-------------------------------------------------------------------------------------------------------------------
    //esta funcion abre la ventana emergente
    $('#boton_registrarse').click(function() {
        const size = "width=800,height=500";
        window.open("registrarse.html", "Iniciar Sesión", size);
    });



    $('#formulario_registro').submit(function(event) {
        event.preventDefault();
        
        //cargamos los valores introducidos
        let nombre_usuario = $("#nombre_usuario_new").val();
        let password = $("#password_new").val();
        let password_repe=$("#password_repe").val();
        let correo = $("#correo_new").val();
        let ciudad = $("#ciudad_new").val();
        let pais = $("#pais_new").val();
        let genero = $("#genero_new").val();

        //antes de crear un JSON para el nuevo registro, verificamos que las variables sean correctas:
        let input_validos = true;
        //intentamos ponerlo primero en false y cambiarlo a true una vez pasadas todas las restricciones pero no iba :(

        //VALIDAMOS PASSWORD (con función externa no funcionaba, por eso esta aquí dentro)-----------------
        //restricciones de la contraseña
        const nums = (password.match(/[0-9]/g) || []).length; //tamaño del array que contiene todos los números metidos en la contraseña
        const mayus = /[A-Z]/.test(password); //booleano, true si detecta alguna mayúscula
        const minus = /[a-z]/.test(password); //booleano, para minúsculas
        const especiales = /[_@.%]/.test(password); //consideraremos especiales _ . @ y %
        //-------------------------------------------------------------------------------------------------

        //lo hacemos con else if para que no salten todas las alertas de golpe si hubiera varias
        //NOTA: el correo se valida directamente en el .html
        if (nombre_usuario.length < 3) {
        alert("Nombre mínimo 3 caracteres");
        input_validos = false;
        } else if (password.length != 12 || nums < 2 || mayus==false || minus==false || especiales==false){
        alert("La contraseña debe contener 12 caracteres y al menos dos números, una mayúscula, una minúscula y un caracter especial (_ . @ %)");
        input_validos = false;
        } else if (password != password_repe){
        alert("Las contraseñas no coinciden")
        input_validos = false;
        } else if (ciudad.length < 3) {
        alert("Ciudad mínimo 3 caracteres");
        input_validos = false;
        } else if (pais.length < 3) {
        alert("Pais mínimo 3 caracteres");
        input_validos = false;
        }
        
        //si todo está bien, seguimos
        if (input_validos){
        var usuario_datos = {
            nombre_usuario: nombre_usuario,
            password: password,
            correo: correo,
            ciudad: ciudad,
            pais: pais,
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
            
            window.close();
        }
        else if (usuario_ya_existente){
            alert("Este usuario ya está registrado");
        }
        }
    });


    
    //boton cancelar
    $("#cancelar_crear_usuario").click(function() {
        if (confirm("¿Estás seguro de que deseas cancelar? Todos los cambios se perderán.")) {
            window.close();
        }
    });



    // boton limpiar
    $("#limpiar_formulario").click(function() {
        if (confirm("¿Borrar datos?")) {
            $("#formulario_registro")[0].reset();
        }
    });



    //función para añadir campos al html por cada niño que tengas
    $("#hijos_new").on("input", function() {
        let hijos = $(this).val(); //numero hijos
        let div_hijos = $("#datos_hijos");
        div_hijos.empty(); //vaciamos el contenedor de posibles iteraciones anteriores

        if (hijos > 0){
        for (let i = 1; i <= hijos; i++){
            let formulario = $("<div></div>").attr({id: "hijo_nuevo"});

            let label_nombre = $("<label></label>").attr("for", "nombre" + i).text("Nombre hijo " + i + ":");
            let input_nombre = $("<input>").attr({type: "text", id: "nombre" + i, minlength: 3});
            formulario.append(label_nombre).append(input_nombre);

            let label_edad = $("<label></label>").attr("for", "edad" + i).text("Edad " + i + ":");
            let input_edad = $("<input>").attr({type: "number", id: "edad" + i});
            formulario.append(label_edad).append(input_edad);

            let label_juguete = $("<label></label>").attr("for", "juguete" + i).text("Juguete favorito " + i + ":");
            let input_juguete = $("<input>").attr({type: "text", id: "juguete" + i});
            formulario.append(label_juguete).append(input_juguete);

            div_hijos.append(formulario);
        }
        }
    });
});