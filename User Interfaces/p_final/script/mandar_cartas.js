$(document).ready(function(){
    // Verificamos que sesión iniciada esté en localStorage. Si no está, la inicializamos a false
    //if (!localStorage.getItem("sesion_iniciada")) {
    //    localStorage.setItem("sesion_iniciada", "false");
    //}

    // chequeamos el formulario
    $('#formulario-buzon').on("submit", function(e){
        e.preventDefault();

        //cogemos los valores introducidos
        let nombre = $("#nombre").val();
        let apellidos = $("#apellidos").val();
        let mail = $("#mail").val();
        let carta = $("#carta").val();

        // ahora cogemos los datos del formulario
        let usuarios_guardados = JSON.parse(localStorage.getItem('usuarios')) || []; //json todos los usuarios
        let username = localStorage.getItem("usuario_iniciado"); //nombre usuario registrado
        let sesion_iniciada = localStorage.getItem("sesion_iniciada"); //bool que indica si hemos iniciado sesion
        let datosFormulario = JSON.parse(localStorage.getItem("datosFormulario")) || []; //cartas de los usuarios
        
        let input_validos = true;

        //evitar campos vacíos
        if ((mail.trim() === "")||(nombre.trim() === "")||(apellidos.trim() === "") || (carta.trim() === "")){
            e.preventDefault();
            alert("¡No dejes campos vacíos!");
            $(this).trigger("reset");
            return;
        }
        
        // comprobamos que la sesión esté iniciada, y no permitimos mandar si no lo está
        if(!sesion_iniciada){
            alert("¡Inicia sesión para poder mandar cartas!");
            //return;
        }

        for (let i = 0; i < usuarios_guardados.length; i++){
            if (usuarios_guardados[i].nombre_usuario == username){ // si encontramos al usuario iniciado en la lista
                if (usuarios_guardados[i].correo != mail){ //checkeamos que los mails coincidan
                    alert("Utiliza el correo registrado en tu cuenta");
                    input_validos = false;
                }
            }
        }
        
        if (input_validos){
            let carta_usuario = {
                usuario: username,
                nombre: nombre,
                carta: carta
            };

            // metemos los datos recogidos en datosFormulario y los ponemos en localStorage
            datosFormulario.push(carta_usuario);
            localStorage.setItem("datosFormulario", JSON.stringify(datosFormulario));

            // guardamos una variable que nos indique cuantas cartas hay de este usuario
            //let n = localStorage.getItem("numCartas") || 0;
            //n++;
            //localStorage.setItem("numCartas", n);

            // mandamos carta y reiniciamos formulario
            alert("¡Tu carta va camino a casa de Papa Noel! (Refresca la web para verla en tu perfil)");
            $(this).trigger("reset");

        } else {
            alert("Error");
        }
    })
});