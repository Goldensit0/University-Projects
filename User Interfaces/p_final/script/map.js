
$(document).ready(function () {
    // vamos a usar leaflet para implementar el mapa, junto con el api de thunderforest
    // pongo las coordenadas iniciales en mi mapa, las de Laponia
    const mapa = L.map("objeto-mapa").setView([67, 26], 4);

    // Ahora uso thunderforest con mi clave privada del API. Hemos iniciado sesión con la versión gratuita
    L.tileLayer('https://tile.thunderforest.com/cycle/{z}/{x}/{y}.png?apikey=86dc6d15a54f4278a5387b0ef6cd794c', {
        attribution: '&copy; Thunderforest contributors'
    }).addTo(mapa);

    // definimos la variable que hará de marcador: Un monigote de papá noel
    let marcadorImagen = L.icon({
        /*iconUrl: "../images/sigue_santa.png",*/
        iconUrl: "images/sigue_santa.png",
        iconSize: [60, 60],
        iconAnchor: [25, 50]
    })
    // definimos el marcador inicial
    let marker = L.marker([67, 26], { icon: marcadorImagen }).addTo(mapa)

    // defino un conjunto de estados a los que va a moverse el marcador
    let estados = [[300, 120],[80, 240], [55, 40], [16, 323], [32, 122], [755, 12] ]
    pos = [67, 26];
    setInterval(()=>{
        function numRandom(min, max) {
            return Math.floor(Math.random() * (max - min + 1)) + min;
        }
        let rand = numRandom(0, estados.length - 1);
        let pos_nueva = estados[rand];

        if(pos_nueva[0] !== pos[0] && pos_nueva[1] !== pos[1]){
            // gestionamos el X:
            if (pos_nueva[0] > pos[0]){
                pos[0]++;
            }
            else{
                pos[0]--;
            }

            // ahora el Y
            if (pos_nueva[1] > pos[1]){
                pos[1]++;
            }
            else{
                pos[1]++;
            }

        }

        marker.setLatLng(pos);
        marker.remove();
        marker = L.marker([pos[0], pos[1]], { icon: marcadorImagen }).addTo(mapa)
    }, 500);

    /*
    // función que crea un camino aleatorio teniendo en cuenta la posicion que ya tiene y su latitud,
    // también coge como argumentos los puntos que habrá por el camino y el radio de km
    function crearCamino(start, puntos, radio) {
        let camino = [start]; // Inicializamos el camino con la posición inicial
        // calculamos las coordenadas que se generarán del camino a seguir
        for (let i = 1; i < puntos; i++) {
            // las operaciones son aproximaciones de los kilómetros por grado de latitud (calculado con ayuda de un chatbox de IA generativa)
            let latitudNew = start[0] + (Math.random() - 0.5) * (radio / 111000);
            let longNew = start[1] + (Math.random() - 0.5) * (radio / (111000 * Math.cos(start[0] * Math.PI / 180)));
            camino.push([latitudNew, longNew]);
        }
        return camino;
    }

    // creamos el camino aleatoriamente partiendo de la casa de santa: Laponia:
    let camino = crearCamino([67, 26], 20, 500);


    // función que mueve el marcador dado el camino que hemos calculado arriba, en un intervalo
    function moverMarcador(marcador, camino, intervalo) {
        let i = 0;
        function animar() {
            if (i < camino.length) {
                marcador.setLatLng(camino[i]);
                i++;
                setTimeout(animar, intervalo);
            }
        }
        animar();
    }


    moverMarcador(marker, camino, 1000);*/

});