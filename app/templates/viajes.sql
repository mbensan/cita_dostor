-- Obtengo los datos de UN viaje
select * from trips
join users on  trips.creator_id = users.id
where id = 4;

-- Obtengo los pasajeros de ese viaje (4)
select * from users
join viaja_hacia on viaja_hacia.user_id = users.id
where viaja_hacia.trip_id = 4;

Maca
Arturo
Ricardo
Flavio
Pablo
Vicente
Karina -> Mail
Eduardo
Rafael -> Mail
Felipe