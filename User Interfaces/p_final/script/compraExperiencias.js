$(document).ready(function(){

    $('#cesta').click(function(){
        let padre = this.parentElement;
        let alturaNavBar = padre.getBoundingClientRect().height;
        let alturaWeb = window.innerHeight;
        let alturaCesta = alturaWeb - alturaNavBar;
        $('.pop-modal-cesta').css('top', alturaNavBar + 'px');
        $('.pop-modal-cesta').css('height', alturaCesta + 'px');
        if ($('.pop-modal-cesta').css('display')==='none'){
            $('.pop-modal-cesta').css('display', 'flex');
        }
        else {
            $('.pop-modal-cesta').hide()
        }

    })

    //ACTUALIZAMOS LA CANTIDAD DE PRODUCTOS CUANDO AÑADIMOS A LA CESTA
    $('.añadir-producto').click(function(){
        let textoOld = Number($('.ribbon').text());
        textoOld += 1;
        let idExperiencia = this.id;
        let id = idExperiencia.replace("añadir", "plus");
        id = '#'+id;
        let cantidadProd = Number($(id).text())
        if (cantidadProd === 0) {
            let cajaProd = idExperiencia.replace("añadir", "producto");
            $('#' + cajaProd).css('display', 'grid');
        }
        cantidadProd +=1;
        $('.ribbon').text(textoOld);
        $(id).text(cantidadProd);

        let idPadre = idExperiencia.replace("añadir", "precio")
        sumarPrecioTotal(idPadre);

        //ACTUALIZAR PRECIO TOTAL

    })

    $('.no-producto').click(function () {
        let idPadre = this.parentElement.id;
        let plus = idPadre.replace("producto", "plus");
        let cantidad = Number($('#'+plus).text());
        let cesta = Number($('.ribbon').text());
        restarPrecioTotal(idPadre)
        cesta -= cantidad;
        $('.ribbon').text(cesta);
        //reseteamos la cantidad
        $('#'+plus).text(0);
        $('#'+idPadre).hide();


        //ACTUALIZAR PRECIO TOTAL

    })

    $('.sumar-producto').click(function () {
        let idPadre = this.parentElement.id;
        let plus = idPadre.replace("producto", "plus");
        let cantidad = Number($('#'+plus).text());
        let cesta = Number($('.ribbon').text());
        cesta += 1;
        cantidad += 1
        $('.ribbon').text(cesta);
        //reseteamos la cantidad
        $('#'+plus).text(cantidad);
        idPadre = idPadre.replace("producto", "precio")
        sumarPrecioTotal(idPadre);
        //ACTUALIZAR PRECIO TOTAL
    })

    function sumarPrecioTotal(idPadre){
        let precio = $('#'+idPadre).text().replace("$","");
        precio = Number(precio);
        let totalPrecio = $('#span-total').text().replace("$","");
        totalPrecio = Number(totalPrecio)
        totalPrecio += precio;
        $('#span-total').text('$'+totalPrecio);
    }

    function restarPrecioTotal(idPadre){
        let precioId = idPadre.replace("producto", "precio");
        let precio = $('#'+precioId).text().replace("$","");
        precio = Number(precio);
        let totalPrecio = $('#span-total').text().replace("$","");
        totalPrecio = Number(totalPrecio)
        let cantidadProd = idPadre.replace("producto", "plus");
        cantidadProd = Number($('#'+cantidadProd).text());
        let cantidadRestar = cantidadProd * precio;
        totalPrecio -= cantidadRestar;
        $('#span-total').text('$'+totalPrecio);
    }

    $('#pagar-boton').click(function () {
        let siUsuario = JSON.parse(localStorage.getItem("sesion_iniciada")) || [];
        let cantidadprod = Number($('.ribbon').text());
        if (siUsuario === true && cantidadprod > 0) {
            $('#pago-pop-up').show();
            let dinero = $('#span-total').text()
            $('#pago-boton').text('Pagar '+ dinero );

        }
        else if (cantidadprod === 0){
            window.alert('Por favor, añada algún producto')
        }
        else {
            window.alert('Por favor, inicie sesión primero')
        }
    })

    $('#cerrar-pago').click(function (){
        $('#pago-pop-up').hide();
    })

    $('#pago-form').submit(function (e) {
        e.preventDefault();
        let hoy = new Date()
        hoy = hoy.toDateString()
        console.log(hoy)
        //cargamos los valores introducidos
        let nombre = $("#nombre-pago").val();
        let correo = $("#email-pago").val();
        let pais = $("#pais-pago").val();
        let ciudad = $("#ciudad-pago").val();
        let dic = $("#dirc-pago").val();

        //VALIDAMOS
        //restricciones de la contraseña

        let input_no_validos = true;
        //lo hacemos con else if para que no salten todas las alertas de golpe si hubiera varias
        //NOTA: el correo se valida directamente en el .html
        if (nombre.length < 3) {
            alert("Nombre mínimo 3 caracteres");
            input_no_validos = false;
        } else if (ciudad.length < 3) {
            alert("Ciudad mínimo 3 caracteres");
            input_no_validos = false;
        }else if (pais.length < 3) {
            alert("País mínimo 3 caracteres");
            input_no_validos = false;
        }else if (dic.length < 3) {
            alert("Dirección mínimo 3 caracteres");
            input_no_validos = false;
        }



        //si lelgamos aquí todos los datos eran correctos, creamos al usuario
        if (input_no_validos){
            var compra = {
                fecha: hoy,
                "producto-peluche-papa": Number($('#plus-peluche-papa').text()),
                "producto-calendario": Number($('#plus-calendario').text()),
                "producto-peluche-rodolfo": Number($('#plus-peluche-rodolfo').text()),
                "producto-libro": Number($('#plus-libro').text()),
                "producto-viaje": Number($('#plus-viaje').text()),
                "producto-elfo": Number($('#plus-elfo').text())
            };
            let usuario = localStorage.getItem('usuario_iniciado');
            let compras_usuario = JSON.parse(localStorage.getItem(usuario +'_compras')) || [];
            compras_usuario.push(compra);
            // guardar en local storage
            localStorage.setItem(usuario+'_compras', JSON.stringify(compras_usuario));
            // reseteamos la cesta para futuras compra
            $('.ribbon').text(0)
            restarPrecioTotal('producto-peluche-papa')
            $('#producto-peluche-papa').hide()
            restarPrecioTotal("producto-calendario")
            $('#producto-calendario').hide()
            restarPrecioTotal("producto-peluche-rodolfo")
            $('#producto-peluche-rodolfo').hide()
            restarPrecioTotal("producto-libro")
            $('#producto-libro').hide()
            restarPrecioTotal("producto-viaje")
            $('#producto-viaje').hide()
            restarPrecioTotal("producto-elfo")
            $('#producto-elfo').hide()
            //reseteamos toda la cestas
            $('#pago-pop-up').hide();
            $('#cesta-pop-up').hide();
            alert("Ha realizado la compra exitosamente :)");
        }
        
        

    })
    
    function crearHistorial() {

    }
})