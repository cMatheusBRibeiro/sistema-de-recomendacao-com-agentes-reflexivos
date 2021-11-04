CREATE DATABASE sistemarecomendacao;
USE sistemarecomendacao;

CREATE TABLE produto (
    idProduto INT AUTO_INCREMENT PRIMARY KEY,
    descricao VARCHAR(50)
)ENGINE=INNODB;

CREATE TABLE recomendacao (
    idRecomendacao INT AUTO_INCREMENT PRIMARY KEY,
    produtoRecomendado INT,
    FOREIGN KEY (produtoRecomendado)
        REFERENCES produto (idProduto)
)ENGINE=INNODB;

CREATE TABLE produtoRecomendacao(
    idProduto INT,
    idRecomendacao INT,
    FOREIGN KEY (idProduto)
        REFERENCES produto (idProduto),
    FOREIGN KEY (idRecomendacao)
        REFERENCES recomendacao (idRecomendacao)
)ENGINE=INNODB;

CREATE TABLE transacao (
    idTransacao INT AUTO_INCREMENT PRIMARY KEY,
    data DATETIME,
    periodo_dia VARCHAR(20),
    weekday_weekend VARCHAR(20)
)ENGINE=INNODB;

CREATE TABLE produtoTransacao (
    idProdutoTransacao INT AUTO_INCREMENT PRIMARY KEY,
    idProduto INT,
    idTransacao INT,
    FOREIGN KEY (idProduto)
        REFERENCES produto (idProduto),
    FOREIGN KEY (idTransacao)
        REFERENCES transacao (idTransacao)
)ENGINE=INNODB;
