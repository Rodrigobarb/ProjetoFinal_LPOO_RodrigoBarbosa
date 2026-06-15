-- ============================================================
-- LPOO 2026-1 - Sistema de Gerenciamento de Arena Games
-- Banco: lpoo_projeto_arena_games
-- ============================================================

-- 1. CRIAR BANCO (executar separadamente se necessário)
-- CREATE DATABASE lpoo_projeto_arena_games;

-- 2. TABELA DE JOGOS
CREATE TABLE IF NOT EXISTS tb_jogos (
    jog_id SERIAL PRIMARY KEY,
    jog_nome VARCHAR(100) NOT NULL,
    jog_genero VARCHAR(50) NOT NULL,
    jog_plataforma VARCHAR(50) NOT NULL,
    jog_max_jogadores_equipe INTEGER NOT NULL CHECK (jog_max_jogadores_equipe > 0)
);

-- 3. TABELA DE EQUIPES
CREATE TABLE IF NOT EXISTS tb_equipes (
    equ_id SERIAL PRIMARY KEY,
    equ_nome VARCHAR(100) NOT NULL UNIQUE,
    equ_data_criacao DATE NOT NULL,
    equ_jogo_id INTEGER NOT NULL,
    CONSTRAINT fk_equipe_jogo FOREIGN KEY (equ_jogo_id) 
        REFERENCES tb_jogos(jog_id) ON DELETE RESTRICT
);

-- 4. TABELA DE JOGADORES
CREATE TABLE IF NOT EXISTS tb_jogadores (
    jgd_id SERIAL PRIMARY KEY,
    jgd_nome VARCHAR(100) NOT NULL,
    jgd_cpf VARCHAR(14) NOT NULL UNIQUE,
    jgd_nickname VARCHAR(50) NOT NULL UNIQUE,
    jgd_equipe_id INTEGER NOT NULL,
    CONSTRAINT fk_jogador_equipe FOREIGN KEY (jgd_equipe_id) 
        REFERENCES tb_equipes(equ_id) ON DELETE CASCADE
);

-- 5. TABELA DE TORNEIOS
CREATE TABLE IF NOT EXISTS tb_torneios (
    tor_id SERIAL PRIMARY KEY,
    tor_nome VARCHAR(100) NOT NULL,
    tor_data_inicio DATE NOT NULL,
    tor_status VARCHAR(20) NOT NULL DEFAULT 'ABERTO' 
        CHECK (tor_status IN ('ABERTO', 'EM_ANDAMENTO', 'FINALIZADO')),
    tor_tipo VARCHAR(30) NOT NULL CHECK (tor_tipo IN ('ELIMINACAO', 'PONTOS')),
    tor_jogo_id INTEGER NOT NULL,
    CONSTRAINT fk_torneio_jogo FOREIGN KEY (tor_jogo_id) 
        REFERENCES tb_jogos(jog_id) ON DELETE RESTRICT
);

-- 6. TABELA DE INSCRIÇÕES (N-N entre Equipe e Torneio)
CREATE TABLE IF NOT EXISTS tb_inscricoes (
    ins_id SERIAL PRIMARY KEY,
    ins_equipe_id INTEGER NOT NULL,
    ins_torneio_id INTEGER NOT NULL,
    ins_data_inscricao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_inscricao_equipe FOREIGN KEY (ins_equipe_id) 
        REFERENCES tb_equipes(equ_id) ON DELETE CASCADE,
    CONSTRAINT fk_inscricao_torneio FOREIGN KEY (ins_torneio_id) 
        REFERENCES tb_torneios(tor_id) ON DELETE CASCADE,
    CONSTRAINT uk_inscricao_unica UNIQUE (ins_equipe_id, ins_torneio_id)
);

-- 7. TABELA DE PARTIDAS
CREATE TABLE IF NOT EXISTS tb_partidas (
    par_id SERIAL PRIMARY KEY,
    par_torneio_id INTEGER NOT NULL,
    par_fase VARCHAR(30) NOT NULL,
    par_equipe1_id INTEGER NOT NULL,
    par_equipe2_id INTEGER NOT NULL,
    par_vencedor_id INTEGER,
    CONSTRAINT fk_partida_torneio FOREIGN KEY (par_torneio_id) 
        REFERENCES tb_torneios(tor_id) ON DELETE CASCADE,
    CONSTRAINT fk_partida_equipe1 FOREIGN KEY (par_equipe1_id) 
        REFERENCES tb_equipes(equ_id) ON DELETE RESTRICT,
    CONSTRAINT fk_partida_equipe2 FOREIGN KEY (par_equipe2_id) 
        REFERENCES tb_equipes(equ_id) ON DELETE RESTRICT,
    CONSTRAINT fk_partida_vencedor FOREIGN KEY (par_vencedor_id) 
        REFERENCES tb_equipes(equ_id) ON DELETE SET NULL
);

-- 8. ÍNDICES PARA OTIMIZAÇÃO
CREATE INDEX IF NOT EXISTS idx_equipes_jogo ON tb_equipes(equ_jogo_id);
CREATE INDEX IF NOT EXISTS idx_jogadores_equipe ON tb_jogadores(jgd_equipe_id);
CREATE INDEX IF NOT EXISTS idx_torneios_status ON tb_torneios(tor_status);
CREATE INDEX IF NOT EXISTS idx_torneios_jogo ON tb_torneios(tor_jogo_id);
CREATE INDEX IF NOT EXISTS idx_inscricoes_torneio ON tb_inscricoes(ins_torneio_id);
CREATE INDEX IF NOT EXISTS idx_partidas_torneio ON tb_partidas(par_torneio_id);

-- 9. DADOS DE EXEMPLO
INSERT INTO tb_jogos (jog_nome, jog_genero, jog_plataforma, jog_max_jogadores_equipe) VALUES
('League of Legends', 'MOBA', 'PC', 5),
('Counter-Strike 2', 'FPS', 'PC', 5),
('Valorant', 'FPS', 'PC', 5),
('Rocket League', 'Esporte', 'Multi', 3),
('FIFA 24', 'Esporte', 'Multi', 1);

INSERT INTO tb_equipes (equ_nome, equ_data_criacao, equ_jogo_id) VALUES
('Loud', '2022-01-15', 1),
('FURIA', '2017-08-01', 2),
('paiN Gaming', '2010-09-12', 1),
('MIBR', '2003-01-01', 2);

INSERT INTO tb_jogadores (jgd_nome, jgd_cpf, jgd_nickname, jgd_equipe_id) VALUES
('Gabriel Lima', '123.456.789-09', 'brTT', 1),
('Felipe Gonçalves', '987.654.321-00', 'FalleN', 2),
('Lucas Teles', '111.222.333-44', 'Robo', 3),
('Fernando Alvarenga', '555.666.777-88', 'fer', 4);

INSERT INTO tb_torneios (tor_nome, tor_data_inicio, tor_status, tor_tipo, tor_jogo_id) VALUES
('Campeonato Brasileiro LoL 2026', '2026-03-01', 'ABERTO', 'ELIMINACAO', 1),
('Copa CS2 Sul', '2026-04-15', 'ABERTO', 'PONTOS', 2);

INSERT INTO tb_inscricoes (ins_equipe_id, ins_torneio_id) VALUES
(1, 1),
(3, 1),
(2, 2),
(4, 2);

INSERT INTO tb_partidas (par_torneio_id, par_fase, par_equipe1_id, par_equipe2_id, par_vencedor_id) VALUES
(1, 'SEMIFINAL', 1, 3, NULL);
