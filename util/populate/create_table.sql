create table acoes_e_cotacoes.info_acoes
(
    id        serial
        constraint info_pk
            primary key,
    texto     varchar,
    nome_cota varchar
);

alter table acoes_e_cotacoes.info_acoes
    owner to postgres;

create table acoes_e_cotacoes.historico
(
    idhistoric serial
        constraint historico_pk
            primary key,
    data       date,
    valor_cota money,
    rendimento money,
    nome_cota  varchar not null
);

alter table acoes_e_cotacoes.historico
    owner to postgres;

create table acoes_e_cotacoes.vinculo
(
    idvinculo serial
        constraint vinculo_pk
            primary key,
    vinculos  varchar,
    nome_cota varchar
);

alter table acoes_e_cotacoes.vinculo
    owner to postgres;

create table acoes_e_cotacoes.acoes_historico
(
    id_acoes     integer not null
        constraint acoes_un
            unique,
    id_historico integer not null
        constraint historico_un
            unique
        constraint acoes_historico_fk
            references acoes_e_cotacoes.historico
            on update cascade on delete cascade
);

alter table acoes_e_cotacoes.acoes_historico
    owner to postgres;

create table acoes_e_cotacoes.acoes
(
    idacao              serial
        constraint acao_pk
            primary key
        constraint acoes_fk
            references acoes_e_cotacoes.acoes_historico (id_acoes)
            on update cascade on delete cascade,
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
    info_id             integer
        constraint info_fk
            references acoes_e_cotacoes.info_acoes
            on update cascade on delete cascade,
    historico_id        integer,
    vinculo_id          integer
        constraint vinculo_fk
            references acoes_e_cotacoes.vinculo
            on update cascade on delete cascade
);

alter table acoes_e_cotacoes.acoes
    owner to postgres;

