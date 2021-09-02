# sistema-de-recomendacao-com-agentes-reflexivos

Este repositório se destina a armazenar os arquivos e atualizações de um sistema de recomendação, escrito em python 3.9.6.

## Descrição

Este sistema possui um sistema simples de produto -> recomendação no qual, ao finalizar a compra, verificará todas as recomendações inseridas no banco de dados e, para cada recomendação, se os produtos presentes no carrinho também estão presentes no carrinho. Após essa verificação, será feita a verificação de se o produto a ser recomendado também está presente no carrinho, caso não esteja, será recomendado e o usuário poderá adicioná-lo.

O banco de dados utilizado nesta aplicação foi o MariaDB possuindo três tabelas, sendo elas a tabela de produto, produtoRecomendacao e recomendacao.
