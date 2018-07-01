CREATE DATABASE IF NOT EXISTS augur CHARACTER SET utf8;

use augur;

CREATE TABLE IF NOT EXISTS all_coins (
    coin_id VARCHAR(8) PRIMARY KEY,
    code VARCHAR(16)
);

CREATE TABLE IF NOT EXISTS all_symbols (
    symbol_id VARCHAR(16) PRIMARY KEY,
    symbol VARCHAR(16)
);

CREATE TABLE IF NOT EXISTS kline_15min (
    symbol_id VARCHAR(16),
    amount FLOAT, 
    close_price FLOAT, 
    max_price FLOAT, 
    min_price FLOAT, 
    open_price FLOAT, 
    pre_close_price FLOAT, 
    `timestamp` INTEGER UNSIGNED, 
    usdt_amount FLOAT, 
    volume FLOAT,
    FOREIGN KEY fk_symbol_id(symbol_id)
    REFERENCES all_symbols(symbol_id) 
    ON UPDATE CASCADE,
    PRIMARY KEY (`symbol_id`, `timestamp`)
);

CREATE TABLE IF NOT EXISTS kline_60min (
    symbol_id VARCHAR(16),
    amount FLOAT, 
    close_price FLOAT, 
    max_price FLOAT, 
    min_price FLOAT, 
    open_price FLOAT, 
    pre_close_price FLOAT, 
    `timestamp` INTEGER UNSIGNED, 
    usdt_amount FLOAT, 
    volume FLOAT,
    FOREIGN KEY fk_symbol_id(symbol_id)
    REFERENCES all_symbols(symbol_id) 
    ON UPDATE CASCADE,
    PRIMARY KEY (`symbol_id`, `timestamp`)
)