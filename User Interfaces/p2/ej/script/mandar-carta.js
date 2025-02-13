$(document).ready(function() {
    
    $("#form_enviar_carta").submit(function(event){
        event.preventDefault();
        /*IDEA
        para mandar la carta, primero checkeamos que hay un usuario con la sesion iniciada, buscamos su nombre
        en la base de datos y comprobamos además que el correo coincida con eñ suyo.
        si es la primera carta, creamos un array en local storage consistente en su nombre de usuario y una lista con sus cartas. 
        Si no es la primera que manda, simplemente appendeamos.
        Luego de alguna manera en la funcion del popup mis cartas las sacamos del array este*/
        
        //cargamos los valores introducidos
        let nombre = $("#nombre").val();
        let email = $("#email").val();
        let ciudad=$("#ciudad").val();
        let pais = $("#pais").val();
        let carta = $("#carta").val();

        //cargo el array de usuarios, para comprobar mail
        //debe coincidir con el mail del usuario registrado    
        let usuarios_guardados = JSON.parse(localStorage.getItem("usuarios")) || [];
        let nombre_usuario_iniciado_sesion = localStorage.getItem("usuario_iniciado");
        let usuario_iniciado_sesion = localStorage.getItem("sesion_iniciada"); //bool
        let cartas_usuarios = JSON.parse(localStorage.getItem("cartas")) || [];
        
        let input_validos = true;

        //checkeamos el correo, la unica variable condicionante
        if (!usuario_iniciado_sesion){
            alert("Debes estar registrado para mandar una carta");
        }
        
        for (let i = 0; i < usuarios_guardados.length; i++){
            if (usuarios_guardados[i].nombre_usuario == nombre_usuario_iniciado_sesion){
                if (usuarios_guardados[i].correo != email){
                    alert("Utiliza el correo registrado en tu cuenta");
                    input_validos = false;
                    }
                }
        }
        
        if (input_validos){
            //array que guardaremos
            let carta_usuario = {
                usuario: nombre_usuario_iniciado_sesion,
                nombre:nombre,
                ciudad:ciudad,
                pais:pais,
                carta: carta
            };
            
            //ubicacion donde lo guardaremos
            cartas_usuarios.push(carta_usuario);
            localStorage.setItem("cartas", JSON.stringify(cartas_usuarios));
            alert("Carta subida. Por favor, actualice la web para verla en su perfil."); 
        } else{
            alert("Error");
        }
    });

});