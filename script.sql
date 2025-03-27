CREATE TABLE operadoras (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cnpj VARCHAR(14) UNIQUE,
    razao_social VARCHAR(255),
    categoria VARCHAR(255),
    status VARCHAR(50),
    data_inclusao DATE,
    endereco VARCHAR(255),
    municipio VARCHAR(255),
    uf VARCHAR(2),
    telefone VARCHAR(20),
    email VARCHAR(100)
);

CREATE TABLE despesas (
    id SERIAL PRIMARY KEY,
    operadora_id INT NOT NULL,
    categoria_despesa VARCHAR(255),
    valor DECIMAL(15, 2),
    trimestre INT,
    ano INT,
    FOREIGN KEY (operadora_id) REFERENCES operadoras(id) ON DELETE CASCADE
);


LOAD DATA INFILE '/dados_ans/Relatorio_cadop.csv'
INTO TABLE operadoras
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(nome, cnpj, razao_social, categoria, status, data_inclusao, endereco, municipio, uf, telefone, email);


LOAD DATA INFILE '/dados_ans/1T2024/1T2024.csv'
INTO TABLE despesas
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(operadora_id, categoria_despesa, valor, trimestre, ano);

LOAD DATA INFILE '/dados_ans/1T2024/2T2024.csv'
INTO TABLE despesas
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(operadora_id, categoria_despesa, valor, trimestre, ano);

LOAD DATA INFILE '/dados_ans/3T2024/1T2024.csv'
INTO TABLE despesas
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(operadora_id, categoria_despesa, valor, trimestre, ano);

LOAD DATA INFILE '/dados_ans/4T2024/1T2024.csv'
INTO TABLE despesas
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(operadora_id, categoria_despesa, valor, trimestre, ano);

SELECT o.nome, SUM(d.valor) AS total_despesa
FROM despesas d
JOIN operadoras o ON o.id = d.operadora_id
WHERE d.categoria_despesa = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR'
  AND d.ano = EXTRACT(YEAR FROM CURRENT_DATE)
  AND d.trimestre = EXTRACT(QUARTER FROM CURRENT_DATE)
GROUP BY o.nome
ORDER BY total_despesa DESC
LIMIT 10;

SELECT o.nome, SUM(d.valor) AS total_despesa
FROM despesas d
JOIN operadoras o ON o.id = d.operadora_id
WHERE d.categoria_despesa = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR'
  AND d.ano = EXTRACT(YEAR FROM CURRENT_DATE) - 1
GROUP BY o.nome
ORDER BY total_despesa DESC
LIMIT 10;


