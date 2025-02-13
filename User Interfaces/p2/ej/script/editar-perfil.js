$(document).ready(function() {
    //mostrar perfil si le damos al boton
    $("#b_mi_perfil").click(function() {
        mostrar_datos_usuario();
        $("#popup_mi_perfil").show();

      });

    
    //cerrar pop up si le damos a cancelar
    $("#cancelar_edicion").click(function() {
        $("#popup_mi_perfil").hide();
    });

    //edicion de parametros:

    //------------------USUARIO------------------------
    $("#editar_usuario").click(function() {
      const nuevo = prompt("Nuevo nombre de usuario:");
      //NO PUEDE SER NULL
      if (nuevo === null || nuevo.trim() === "") {
        alert("No se realizó ningun cambio");
        return;
    }

      //REVISAR QUE NO PERTENEZCA A ALGUN USUARIO EXISTENTE
      let usuarios_guardados = JSON.parse(localStorage.getItem('usuarios')) || [];
      let usuario_ya_existente = false;
      
      for (let i = 0; i < usuarios_guardados.length; i++){
        if (usuarios_guardados[i].nombre_usuario == nuevo){
          usuario_ya_existente = true;
        }
      }

      if (!usuario_ya_existente){
        let mi_usuario = localStorage.getItem("usuario_iniciado");
        // busco ese usuario en el array de registrados
        // queremos la posicion del usuario cuyos datos queremos cambiar
        let posicion = null;

        for (let i = 0; i < usuarios_guardados.length; i++){
            if (usuarios_guardados[i].nombre_usuario == mi_usuario){
              //nos quedamos la i para poder actualizar el json
              posicion = i;
            }
        }

        usuarios_guardados[posicion].nombre_usuario = nuevo;

        //por ultimo, cambiamos el valor
        localStorage.setItem("usuarios", JSON.stringify(usuarios_guardados));
        alert("Usuario actualizado. Por favor, cierre sesión y vuelva a loguearse para garantizar el correcto funcionamiento de la web.");
        //debe salir y entrar porque no se cambia el valor de "usuario_iniciado" de localstorage, por lo qeu alguans funciones dejarían de ir
      

      } else {
        alert("Usuario ya existente, prueba con otro nombre");
        return
      }

    });


    //-------------------CORREO-----------------
    $("#editar_correo").click(function() {
      const nuevo = prompt("Nuevo correo:");
      //NO PUEDE SER NULL
      if (nuevo === null || nuevo.trim() === "") {
        alert("No se realizó ningun cambio");
        return;
      }
      //verificamos correo formato correcto
      const email_regex = /^[^@]+@[^@]+\.[a-zA-Z]{2,}/;
      if (!email_regex.test(nuevo)) {
        alert("Formato de correo no válido.");
        return;
      }
      //REVISAR QUE NO PERTENEZCA A ALGUN USUARIO EXISTENTE
      let usuarios_guardados = JSON.parse(localStorage.getItem('usuarios')) || [];
      let mi_usuario = localStorage.getItem("usuario_iniciado");
      // queremos la posicion del usuario cuyos datos queremos cambiar
      let posicion = null;
      let correo_repe = false;
      ///primero buscamos los datos del usuario
      for (let i = 0; i < usuarios_guardados.length; i++){
        if (usuarios_guardados[i].nombre_usuario == mi_usuario){
          posicion = i;
        }
      }
      //ahora, buscamos que el nuevo correo no exista ya en la base de datos
      for (let i = 0; i < usuarios_guardados.length; i++){
          if (usuarios_guardados[i].correo == nuevo){
            //nos quedamos la i para poder actualizar el json
            correo_repe = true;
          }
      }

      if (!correo_repe){
        usuarios_guardados[posicion].correo = nuevo;

        //por ultimo, cambiamos el valor
        localStorage.setItem("usuarios", JSON.stringify(usuarios_guardados));
        alert("Correo actualizado.");
        //debe salir y entrar porque no se cambia el valor de "usuario_iniciado" de localstorage, por lo qeu alguans funciones dejarían de ir

      } else {
        alert("Correo ya registrado, intente otro.");
        return;
      }
    });


    //-------------------CIUDAD-------------------
    $("#editar_ciudad").click(function() {
      const nuevo = prompt("Nueva ciudad:");
      //NO PUEDE SER NULL
      if (nuevo === null || nuevo.trim() === "") {
        alert("No se realizó ningun cambio");
        return;
      }
      //REVISAR QUE NO PERTENEZCA A ALGUN USUARIO EXISTENTE
      let usuarios_guardados = JSON.parse(localStorage.getItem('usuarios')) || [];
      let mi_usuario = localStorage.getItem("usuario_iniciado");
      // queremos la posicion del usuario cuyos datos queremos cambiar
      let posicion = null;

      for (let i = 0; i < usuarios_guardados.length; i++){
          if (usuarios_guardados[i].nombre_usuario == mi_usuario){
            //nos quedamos la i para poder actualizar el json
            posicion = i;
          }
      }
      usuarios_guardados[posicion].ciudad = nuevo;
      //por ultimo, cambiamos el valor
      localStorage.setItem("usuarios", JSON.stringify(usuarios_guardados));
      alert("Ciudad actualizada. Cierre y vuelva a abrir para ver los cambios");
    });


    //-------------------PAÍS-------------------
    $("#editar_pais").click(function() {
      const nuevo = prompt("Nuevo país:");
      //NO PUEDE SER NULL
      if (nuevo === null || nuevo.trim() === "") {
        alert("No se realizó ningun cambio");
        return;
      }
      //REVISAR QUE NO PERTENEZCA A ALGUN USUARIO EXISTENTE
      let usuarios_guardados = JSON.parse(localStorage.getItem('usuarios')) || [];
      let mi_usuario = localStorage.getItem("usuario_iniciado");
      // queremos la posicion del usuario cuyos datos queremos cambiar
      let posicion = null;

      for (let i = 0; i < usuarios_guardados.length; i++){
          if (usuarios_guardados[i].nombre_usuario == mi_usuario){
            //nos quedamos la i para poder actualizar el json
            posicion = i;
          }
      }
      usuarios_guardados[posicion].pais = nuevo;
      //por ultimo, cambiamos el valor
      localStorage.setItem("usuarios", JSON.stringify(usuarios_guardados));
      alert("País actualizado. Cierre y vuelva a abrir para ver los cambios");
    });

    function mostrar_datos_usuario() {
        let mi_usuario = localStorage.getItem("usuario_iniciado");
        
        // busco ese usuario en el array de registrados, para poder mostrar sus datos
        let usuarios_guardados = JSON.parse(localStorage.getItem("usuarios")) || [];

        // aqui guardaremos el array de datos de mi usuario
        let mi_usuario_datos = null;

        for (let i = 0; i < usuarios_guardados.length; i++){
            if (usuarios_guardados[i].nombre_usuario == mi_usuario){
              mi_usuario_datos = usuarios_guardados[i];
            }
          }

        const datos_usuario = `Nombre: ${mi_usuario_datos.nombre_usuario}<br>Correo: ${mi_usuario_datos.correo}<br>Ciudad: ${mi_usuario_datos.ciudad}<br>País: ${mi_usuario_datos.pais}`;

        // lo meto en el <p> reservado para los datos
        $("#datos_usuario").html(datos_usuario);
        
        // Mostrar el pop-up y su info
        $("#popup_mi_perfil_contenido").show();
        $("#popup_mi_perfil").show();
    }
});