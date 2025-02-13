$(document).ready(function() {
    //mostrar cerrar sesion si le damos al boton
    $("#b_mis_cartas").click(function() {
        $("#popup_cartas").show();
      });

    
    //cerrar pop up si le damos a cancelar
    $("#salir_cartas").click(function() {
        $("#popup_cartas").hide();
    });

    mostrar_cartas();
});

function mostrar_cartas(){
    let nombre_usuario_iniciado_sesion = localStorage.getItem("usuario_iniciado");
    let cartas_usuarios = JSON.parse(localStorage.getItem("cartas")) || [];
    let contenedor_cartas = $("#cartas_guardadas");

    // Vaciar el contenedor antes de mostrar nuevas cartas
    contenedor_cartas.empty();

    let num = 1; //pa numerar las cartas

    //añadimos todas las cartas que pertenezcan a nuestro usuario
    for (let i = 0; i < cartas_usuarios.length; i++){
        if (cartas_usuarios[i].usuario == nombre_usuario_iniciado_sesion){
            let carta = $("<div></div>").attr({class: "cajita_carta", id: "cajita_carta"});
            let titulo = $("<h2></h2>").text("Carta " + num + ":");
            let nombre = $("<p></p>").text("Nombre: " + cartas_usuarios[i].nombre);
            let ubi = $("<p></p>").text("Ciudad: " + cartas_usuarios[i].ciudad + " País: " + cartas_usuarios[i].pais);
            let contenido = $("<p></p>").text(cartas_usuarios[i].carta);
            let boton_borrar = $("<button></button>").attr({id:"boton_borrar_carta"}).text("Borrar");
            
            
            carta.append(titulo).append(nombre).append(ubi).append(contenido).append(boton_borrar);
            
            contenedor_cartas.append(carta)

            num++;

            // esta funcion, hace el for num veces y borra esa carta en concreto
            //dentro del for para que se borre la carta seleccionada
            boton_borrar.click(function() {
                let my_index = num-1;
                if (confirm("¿Seguro que quiere borrar la carta?")){
                    borrar_carta(my_index);
                }
            });
            //ESTE APPROACH NO FUNCIONA: SE BORRA SIEMPRE LA ÚLTIMA CARTA
            
        }  
    }
}


function borrar_carta(index) {
    //cargar array cartas
    let cartas_usuarios = JSON.parse(localStorage.getItem("cartas")) || [];
    //let usuario_iniciado = localStorage.getItem("usuario_iniciado")
    
    // creo un array filtrado, solo con las cartas de mi usuario
    //let cartas_del_usuario = cartas_usuarios.filter(carta => carta.usuario === usuario_iniciado);

    //en este nuevo Array, elimino la carta en posición "index"
    //como empezamos a contar por el 1, la posicion que busco será index - 1

    let pos_buscada = index - 1

    cartas_usuarios.splice(pos_buscada, 1);
    
    localStorage.setItem("cartas", JSON.stringify(cartas_usuarios)); // Actualizar localStorage
    mostrar_cartas(); //actualizamos
}

