create database acoes
CREATE SCHEMA acoes_e_cotacoes;
create sequence info;
create table acoes_e_cotacoes.info_acoes
(
    id    serial
        constraint info_pk
            primary key,
    texto varchar
);

create sequence idhistorico;
create table acoes_e_cotacoes.historico
(
    idhistoric  serial
        constraint historico_pk
    	primary key,
    data       date,
    valor_cota money,
    rendimento money
);

create sequence idvinculo;
create table acoes_e_cotacoes.vinculo
(
    idvinculo  serial
        constraint vinculo_pk
        primary key,
    vinculos   varchar
);


create sequence idacao;
create table acoes_e_cotacoes.acoes
(
    idacao   serial
        constraint acao_pk
        primary key,
    name                varchar(50),
    segmento            varchar(50),
    liq_media_day       integer,
    valor_cota          money,
    rendimento          money,
    valor_porcentagem   money,

    porcentagem_divid   money,
    liquidez_d          integer,
    valor_patrimonio_pv money,
    valor_mercado_pv    money,
    rentabilidade       money,
    preco_por_acao      money,
    ultimo_pg           date,
    info_id              integer
        constraint info_fk
            references info_acoes
            on update cascade on delete cascade,
    historico_id        integer
        constraint historico_fk
            references historico
            on update cascade on delete cascade,
    vinculo_id          integer
        constraint vinculo_fk
            references vinculo
            on update cascade on delete cascade
);