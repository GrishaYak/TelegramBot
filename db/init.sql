create table Users(
    tg_username varchar(32) primary key
)

create table Categories(
    id serial unique,
    name varchar(32),
    user_id varchar(32),
    primary key (name, user_id),
    foreign key (user_id) references Users(tg_username) on delete cascade
)

create table Alterations(
    id serial primary key,
    user_id varchar(32),
    category_id int,
    summa int,
    description varchar(255),
    date date,
    foreign key (user_id) references Users(tg_username) on delete cascade,
    foreign key (category_id) references Categories(id) on delete cascade
)