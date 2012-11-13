drop table if exists items;
create table items (
    name string primary key not null,
    location string not null
);

drop table if exists requirements;
create table requirements (
        id integer primary key autoincrement,
        item string references items not null,
        path integer references paths not null
);

drop table if exists paths;
create table paths (
        id integer primary key autoincrement,
        right integer references locations not null,
        left integer references locations not null
);


drop table if exists players;
create table players(
        id integer primary key autoincrement,
        location string not null,
        username string not null,
        password string not null,
        history text not null
);

drop table if exists itemstate;
create table itemstate (
        id integer primary key autoincrement,
        player integer references players not null,
        item string references items not null,
        carried boolean not null,
        lastloc string references locations not null
);

