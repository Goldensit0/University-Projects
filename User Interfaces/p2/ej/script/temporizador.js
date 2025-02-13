class Countdown {
    constructor({givenID, target_date}) {
        this.id = givenID;
        this.target_date = target_date;
    }
    
    getRemainingTime(endtime) { // Calcular tiempo restante
        const time_in_ms = Date.parse(endtime) - Date.parse(new Date());
        const days = Math.floor(time_in_ms / (1000 * 3600 * 24));
        const hours = Math.floor((time_in_ms / (1000 * 3600)) % 24);
        const mins = Math.floor((time_in_ms / 1000 / 60) % 60);
        const secs = Math.floor((time_in_ms / 1000) % 60);
        return {time_in_ms, days, hours, mins, secs};
    }

    updateCountdown({days, hours, mins, secs}) { // Setter
        let time_left = days + " días " + hours + "horas " + mins + "min " + secs + "seg";
        document.getElementById(this.id).innerHTML = time_left;
    }

    interval_function = () => { // función a la que llama el setInterval
        const countdown = this.getRemainingTime(this.target_date);
        this.updateCountdown(countdown);
    }

    start() { // Iniciar el contador
        this.interval_function(); // Valor inicial
        setInterval(this.interval_function, 1000); // Actualizar cada segundo
    }
}

const contador = new Countdown({givenID:"temporizador", target_date: new Date("December, 25 2024 00:00:00"),}); // Crear el contador
contador.start(); // Iniciar el contador