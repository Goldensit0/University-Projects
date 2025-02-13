$(document).ready(function(){

    $('.salir_cartas').click(function(){
        $(".popup_mis_cartas").hide();
    });

    $("#mis_cartas").click(function(){
        $(".popup_mis_cartas").show();
    });

    mostrar_cartas();
});

function mostrar_cartas(){

    // cogemos el número de cartas que hay del user
    //let n =  localStorage.getItem("numCartas") || 0;

    // cogemos las cartas que hay
    let usuarioIniciado = localStorage.getItem("usuario_iniciado");
    let misCartas = JSON.parse(localStorage.getItem("datosFormulario")) || [];
    let contenedor_cartas = $("#contenedor-mis-cartas");

    //if (n === 0){
    //    alert("No tienes cartas, envía alguna!");
    //    return;
    //}

    contenedor_cartas.empty(); //Vaciar el contenedor antes de mostrar nuevas cartas

    let num = 1; //para numerar las cartas

    
    for (let i = 0; i < misCartas.length; i++) {
        if (misCartas[i].usuario === usuarioIniciado){
            let carta = $("<div></div>").attr({class: "contenedor-miscartas-caja"});
            let nombre = $("<h1></h1>").text(misCartas[i].nombre);
            let contenido = $("<p></p>").text(misCartas[i].carta);
            //let boton_borrar = $("<button></button>").attr({id:"boton_borrar_carta"}).text("Borrar");
            //.append(boton_borrar) //para el carta.append
            
            carta.append(nombre).append(contenido);
            contenedor_cartas.append(carta);
            
            num++;
        }
        
    }
}
    
