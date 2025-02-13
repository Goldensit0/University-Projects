$(document).ready(function() {
    $('#historial_compra').click(function () {
        $('#historial-pop-modal').show()
        actualizarHistorial()
    })

    $('#cerrar-historial').click(function () {
        $('#historial-pop-modal').hide()
    })

    function actualizarHistorial(){
        let usuario = localStorage.getItem('usuario_iniciado');
        let compras_usuario = JSON.parse(localStorage.getItem(usuario +'_compras')) || [];
        let contenedor = $('#caja-pedidos').empty()
        let productos = ["producto-peluche-papa", "producto-calendario", "producto-peluche-rodolfo", "producto-libro", "producto-viaje", "producto-elfo"];
        let nombreProductos = ["Peluche Papá Noel", "Calendario de Adviento", "Peluche Rodolfo el Reno", "Libro de colorear", "Viaje a Laponia", "Experiencia Inmersiva (Elfo)"];
        let urlImg = ["images/peluchePapanoel.png", "images/adventCalendar.jpg", "images/pelucheReno.png", "images/coloringBook.jpg", "images/experienciaLaponia.jpg", "images/experienciaElfo.jpg"]

        for (let index = 0; index < compras_usuario.length; index++) {
            let fecha = compras_usuario[index]['fecha'];
            let cajaPedido = $("<div class=\"pedido-historial\">\n")
            cajaPedido.append("<p class=\"fecha-pedido\">Fecha del pedido: " + fecha + "</p>")
            for (let j = 1; j < 6; j++) {
                let producto = compras_usuario[index][productos[j]];
                if (producto !== 0) {
                    cajaPedido.append("<div class=\"caja-productos-historial\">\n" +
                        "                        <h4 class=\"titulo-producto-hist\">" + nombreProductos[j] + "</h4>\n" +
                        "                        <img class=\"img-producto-hist\" src=" + urlImg[j]  + " alt=\"Peluche de Papá Noel\">\n" +
                        "                        <p class=\"texto-producto-hist\">Cantidad:</p>\n" +
                        "                        <p class=\"cant-producto-hist\">" + producto + "</p>\n" +
                        "                    </div>")
                }

            }
            cajaPedido.append("</div>")
            contenedor.append(cajaPedido);
        }

    }

})