set Tarifas;
set Aviones;

param precio_tarifa {i in Tarifas}; # Precio de la tarifa i
param equipaje_tarifa {i in Tarifas}; # Peso máximo de equipaje permitido en la tarifa i
param asientos_avion {j in Aviones}; # Número de asientos en el avión j
param capacidad_avion {j in Aviones}; # Capacidad de carga del avión j

param min_tarifaPorAvion {i in Tarifas}; # Minimo de billetes a vender de la tarifa i
param min_tarifaPercent {i in Tarifas}; # Minimo de billetes a vender de la tarifa i

var billetes {i in Tarifas, j in Aviones} integer >= 0; # Número de billetes vendidos de la tarifa i en el avión j

maximize ingresos: sum{i in Tarifas, j in Aviones} precio_tarifa[i]*billetes[i,j];

/*Restricciones*/

s.t. max_billetes {j in Aviones}: sum{i in Tarifas} billetes[i,j] <= asientos_avion[j]; # No se pueden vender más billetes que asientos
s.t. max_peso {j in Aviones}: sum{i in Tarifas} equipaje_tarifa[i]*billetes[i,j] <= capacidad_avion[j]; # No se puede superar la capacidad de carga del avión
s.t. min_billetesTotal {i in Tarifas, j in Aviones}: billetes[i,j] >= min_tarifaPorAvion[i]; # Se deben vender al menos min_tarifaPorAvion[i] billetes de la tarifa i
s.t. min_billetesPercent {i in Tarifas}: sum{j in Aviones}billetes[i,j] >= min_tarifaPercent[i]*(sum{x in Tarifas, j in Aviones}billetes[x,j]); # Se deben vender al menos min_tarifaPercent[i] por ciento de billetes de la tarifa i

end;