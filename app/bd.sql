CREATE DATABASE sistemarecomendacao;
USE sistemarecomendacao;

CREATE TABLE produto (
    idProduto INT AUTO_INCREMENT PRIMARY KEY,
    descricao VARCHAR(20)
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

INSERT INTO produto (idProduto, descricao) VALUES 
    (1, 'Coxinha'),
    (2, 'Kibe'),
    (3, 'Coca Cola'),
    (4, 'Guaranita'),
    (5, 'Cerveja'),
    (6, 'Vinho'),
    (7, 'Queijo'),
    (8, 'Torresmo'),
    (9, 'Pastel'),
    (10, 'Pão');