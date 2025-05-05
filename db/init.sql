
-- Здесь написаны запросы на создания всех необходимых таблиц.

create table Users(
    tg_username varchar(32) primary key --varchar(X) - это строка, длина которой не больше X символов
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
    user_id varchar(32) not null,
    category_id int not null,
    summa int not null,
    description varchar(255),
    date date not null,
    foreign key (user_id) references Users(tg_username) on delete cascade,
    foreign key (category_id) references Categories(id) on delete cascade
)