CREATE DATABASE sistemarecomendacao;
USE sistemarecomendacao;

CREATE TABLE produto (
    idProduto INT AUTO_INCREMENT PRIMARY KEY,
    descricao VARCHAR(20)
)ENGINE=INNODB;

CREATE TABLE recomendacao (
    idRecomendacao INT AUTO_INCREMENT PRIMARY KEY,
    produtoAnalisado INT,
    produtoRecomendado INT,
    FOREIGN KEY (produtoAnalisado)
        REFERENCES produto (idProduto),
    FOREIGN KEY (produtoRecomendado)
        REFERENCES produto (idProduto)
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