DROP TABLE IF EXISTS web_users;
DROP TABLE IF EXISTS freecoins;


CREATE TABLE web_users (
    username VARCHAR(100),
    password VARCHAR(64),
    coins INT,
    hasFreeCoin BOOLEAN,
    currentToken VARCHAR(64)
);

CREATE TABLE freecoins (
    token VARCHAR(32),
    amount INT
);

insert into web_users (username, password, coins, hasFreeCoin) values ('Dream', 'b398686f5f41c837240a80c6698af961e060210958ceb7b785b38fca9f267f94', 100, true);