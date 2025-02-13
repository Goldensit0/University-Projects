set Tarifas;
set Aviones;
set Pistas;
set Slots;

/* Problema 1 - parametros*/
param precio_tarifa {i in Tarifas}; # Precio de la tarifa i
param equipaje_tarifa {i in Tarifas}; # Peso máximo de equipaje permitido en la tarifa i
param asientos_avion {j in Aviones}; # Número de asientos en el avión j
param capacidad_avion {j in Aviones}; # Capacidad de carga del avión j
param min_tarifaPorAvion {i in Tarifas}; # Minimo de billetes a vender de la tarifa i
param min_tarifaPercent {i in Tarifas}; # Minimo de billetes a vender de la tarifa i

/* Problema 2 - parametros*/
param disponibilidad {p in Pistas, s in Slots}; # Disponibilidad de la pista p en el slot s
param minutosSlot {s in Slots}; # Duración del slot s en minutos
param minAterrizaje {j in Aviones}; # Hora de llegada del avión j
param maxAterrizaje {j in Aviones}; # Hora máxima a la que puede aterrizar el avión j
param costeRetraso {j in Aviones}; # Coste por minuto de retraso del avión j

/* Variables */

var billetes {i in Tarifas, j in Aviones} integer >= 0; # Número de billetes vendidos de la tarifa i en el avión j
var asignado {j in Aviones, p in Pistas, s in Slots} binary; # 1 si el avión j aterriza en el slot s en la pista p, 0 en caso contrario

/* Función objetivo */
maximize ingresos: (sum{i in Tarifas, j in Aviones} precio_tarifa[i]*billetes[i,j]) - (sum{j in Aviones, p in Pistas, s in Slots} (minutosSlot[s]-minAterrizaje[j])*asignado[j,p,s]*costeRetraso[j]);

/* Problema 1 - reestricciones*/

s.t. max_billetes {j in Aviones}: sum{i in Tarifas} billetes[i,j] <= asientos_avion[j]; # No se pueden vender más billetes que asientos
s.t. max_peso {j in Aviones}: sum{i in Tarifas} equipaje_tarifa[i]*billetes[i,j] <= capacidad_avion[j]; # No se puede superar la capacidad de carga del avión
s.t. min_billetesTotal {i in Tarifas, j in Aviones}: billetes[i,j] >= min_tarifaPorAvion[i]; # Se deben vender al menos min_tarifaPorAvion[i] billetes de la tarifa i
s.t. min_billetesPercent {i in Tarifas}: sum{j in Aviones}billetes[i,j] >= min_tarifaPercent[i]*(sum{x in Tarifas, j in Aviones}billetes[x,j]); # Se deben vender al menos min_tarifaPercent[i] por ciento de billetes de la tarifa i

/* Problema 1 - reestricciones*/

s.t. un_slot {j in Aviones}: sum{p in Pistas, s in Slots} asignado[j,p,s] = 1; # Cada avión aterriza en un único slot
s.t. slot_por_avion {p in Pistas, s in Slots}: sum{j in Aviones} asignado[j,p,s] <= 1; # Máximo un slot asignado a un avión
s.t. slot_libre {j in Aviones, p in Pistas, s in Slots}: disponibilidad[p,s] - asignado[j,p,s] >= 0; # No se puede asignar un slot si la pista no está disponible
s.t. aterrizaje_llegada {j in Aviones, p in Pistas, s in Slots}: asignado[j,p,s]*(minutosSlot[s] - minAterrizaje[j]) >= 0; # El avión no puede aterrizar antes de su hora de llegada
s.t. aterrizaje_limite {j in Aviones, p in Pistas, s in Slots}: asignado[j,p,s]*(maxAterrizaje[j] - minutosSlot[s]) >= 0; # El avión no puede aterrizar después de su hora límite
s.t. no_consecutivos {j in Aviones, p in Pistas, s in Slots: s < card(Slots)}: asignado[j,p,s]+asignado[j,p,(s+1)] <= 1; # No se pueden asignar dos slots consecutivos a un avión

end;