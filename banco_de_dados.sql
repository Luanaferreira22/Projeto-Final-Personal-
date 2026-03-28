
--  PERSONAL MANAGER — Gestão de Treinos
--  Banco de Dados SQLite
--  PFC — Sistemas de Informação | UMC — Luana Ferreira — 2026


PRAGMA foreign_keys = ON;


-- 1. USUÁRIOS (tabela nativa do Django Auth)

CREATE TABLE IF NOT EXISTS auth_user (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      VARCHAR(150) NOT NULL UNIQUE,
    email         VARCHAR(254) NOT NULL,
    password      VARCHAR(128) NOT NULL,
    first_name    VARCHAR(150) NOT NULL DEFAULT '',
    last_name     VARCHAR(150) NOT NULL DEFAULT '',
    is_staff      BOOLEAN     NOT NULL DEFAULT 0,
    is_active     BOOLEAN     NOT NULL DEFAULT 1,
    is_superuser  BOOLEAN     NOT NULL DEFAULT 0,
    date_joined   DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login    DATETIME
);


-- 2. ALUNOS

CREATE TABLE IF NOT EXISTS alunos_aluno (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id      INTEGER REFERENCES auth_user(id) ON DELETE SET NULL,
    nome            VARCHAR(100) NOT NULL,
    email           VARCHAR(254) NOT NULL UNIQUE,
    telefone        VARCHAR(20)  NOT NULL DEFAULT '',
    data_nascimento DATE,
    sexo            VARCHAR(1)   NOT NULL DEFAULT 'M',  -- M, F, O
    cep             VARCHAR(9)   NOT NULL DEFAULT '',
    logradouro      VARCHAR(200) NOT NULL DEFAULT '',
    bairro          VARCHAR(100) NOT NULL DEFAULT '',
    cidade          VARCHAR(100) NOT NULL DEFAULT '',
    estado          VARCHAR(2)   NOT NULL DEFAULT '',
    objetivo        TEXT         NOT NULL DEFAULT '',
    ativo           BOOLEAN      NOT NULL DEFAULT 1,
    criado_em       DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_aluno_ativo  ON alunos_aluno(ativo);
CREATE INDEX IF NOT EXISTS idx_aluno_nome   ON alunos_aluno(nome);
CREATE INDEX IF NOT EXISTS idx_aluno_email  ON alunos_aluno(email);


-- 3. EVOLUÇÃO FÍSICA

CREATE TABLE IF NOT EXISTS alunos_evolutionfisica (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id            INTEGER NOT NULL REFERENCES alunos_aluno(id) ON DELETE CASCADE,
    data                DATE    NOT NULL,
    peso                DECIMAL(5,2) NOT NULL,   -- kg  (ex: 75.50)
    altura              DECIMAL(4,2) NOT NULL,   -- m   (ex: 1.75)
    imc                 DECIMAL(4,2),            -- calculado automaticamente
    percentual_gordura  DECIMAL(4,2),            -- % (ex: 18.50)
    observacoes         TEXT NOT NULL DEFAULT '',
    criado_em           DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_evolucao_aluno ON alunos_evolutionfisica(aluno_id);
CREATE INDEX IF NOT EXISTS idx_evolucao_data  ON alunos_evolutionfisica(data);


-- 4. EXERCÍCIOS

CREATE TABLE IF NOT EXISTS treinos_exercicio (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    nome             VARCHAR(100) NOT NULL,
    grupo_muscular   VARCHAR(20)  NOT NULL DEFAULT 'outros',
    -- Valores: peito, costas, ombros, biceps, triceps,
    --          abdomen, gluteos, quadriceps, posterior,
    --          panturrilha, cardio, outros
    descricao        TEXT NOT NULL DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_exercicio_grupo ON treinos_exercicio(grupo_muscular);


-- 5. TREINOS

CREATE TABLE IF NOT EXISTS treinos_treino (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id      INTEGER NOT NULL REFERENCES alunos_aluno(id) ON DELETE CASCADE,
    nome          VARCHAR(100) NOT NULL,
    descricao     TEXT NOT NULL DEFAULT '',
    ativo         BOOLEAN  NOT NULL DEFAULT 1,
    criado_em     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_treino_aluno ON treinos_treino(aluno_id);
CREATE INDEX IF NOT EXISTS idx_treino_ativo ON treinos_treino(ativo);


-- 6. TREINO_EXERCÍCIO (tabela de relacionamento N:N)

CREATE TABLE IF NOT EXISTS treinos_treinoexercicio (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    treino_id    INTEGER NOT NULL REFERENCES treinos_treino(id)    ON DELETE CASCADE,
    exercicio_id INTEGER NOT NULL REFERENCES treinos_exercicio(id) ON DELETE CASCADE,
    series       INTEGER NOT NULL DEFAULT 3,
    repeticoes   VARCHAR(20) NOT NULL DEFAULT '12',  -- ex: "12" ou "8-12"
    carga        DECIMAL(5,2),                        -- kg, pode ser nulo
    descanso     INTEGER NOT NULL DEFAULT 60,         -- segundos
    observacoes  TEXT NOT NULL DEFAULT '',
    ordem        INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_treinoex_treino    ON treinos_treinoexercicio(treino_id);
CREATE INDEX IF NOT EXISTS idx_treinoex_exercicio ON treinos_treinoexercicio(exercicio_id);


-- 7. PLANOS

CREATE TABLE IF NOT EXISTS financeiro_plano (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    nome      VARCHAR(100)  NOT NULL,
    valor     DECIMAL(8,2)  NOT NULL,   -- R$ (ex: 150.00)
    duracao   INTEGER       NOT NULL,   -- dias
    descricao TEXT          NOT NULL DEFAULT '',
    ativo     BOOLEAN       NOT NULL DEFAULT 1
);


-- 8. PAGAMENTOS

CREATE TABLE IF NOT EXISTS financeiro_pagamento (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id        INTEGER NOT NULL REFERENCES alunos_aluno(id)   ON DELETE CASCADE,
    plano_id        INTEGER          REFERENCES financeiro_plano(id) ON DELETE SET NULL,
    valor           DECIMAL(8,2)  NOT NULL,
    data_vencimento DATE          NOT NULL,
    data_pagamento  DATE,                   -- preenchido ao marcar como pago
    pago            BOOLEAN       NOT NULL DEFAULT 0,
    forma_pagamento VARCHAR(20)   NOT NULL DEFAULT '',
    -- Valores: dinheiro, pix, cartao_credito, cartao_debito, transferencia
    observacoes     TEXT          NOT NULL DEFAULT '',
    criado_em       DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_pagamento_aluno      ON financeiro_pagamento(aluno_id);
CREATE INDEX IF NOT EXISTS idx_pagamento_vencimento ON financeiro_pagamento(data_vencimento);
CREATE INDEX IF NOT EXISTS idx_pagamento_pago       ON financeiro_pagamento(pago);


-- DADOS INICIAIS — PLANOS

INSERT OR IGNORE INTO financeiro_plano (nome, valor, duracao, descricao, ativo) VALUES
    ('Plano Mensal',     150.00,  30,  '1 mês de acompanhamento personalizado', 1),
    ('Plano Trimestral', 400.00,  90,  '3 meses com desconto especial',         1),
    ('Plano Semestral',  700.00,  180, '6 meses com maior desconto',            1),
    ('Plano Anual',      1200.00, 365, '12 meses — melhor custo-benefício',     1);


-- DADOS INICIAIS — EXERCÍCIOS

INSERT OR IGNORE INTO treinos_exercicio (nome, grupo_muscular) VALUES
    -- Peito
    ('Supino Reto com Barra',        'peito'),
    ('Supino Inclinado com Halteres','peito'),
    ('Crucifixo',                    'peito'),
    ('Peck Deck',                    'peito'),
    -- Costas
    ('Puxada Frontal',               'costas'),
    ('Remada Curvada',               'costas'),
    ('Remada Unilateral',            'costas'),
    ('Levantamento Terra',           'costas'),
    -- Ombros
    ('Desenvolvimento com Barra',    'ombros'),
    ('Elevação Lateral',             'ombros'),
    ('Elevação Frontal',             'ombros'),
    -- Bíceps
    ('Rosca Direta',                 'biceps'),
    ('Rosca Alternada',              'biceps'),
    ('Rosca Concentrada',            'biceps'),
    -- Tríceps
    ('Tríceps Pulley',               'triceps'),
    ('Tríceps Testa',                'triceps'),
    ('Mergulho no Banco',            'triceps'),
    -- Abdômen
    ('Abdominal Crunch',             'abdomen'),
    ('Prancha',                      'abdomen'),
    ('Abdominal Oblíquo',            'abdomen'),
    -- Glúteos
    ('Agachamento',                  'gluteos'),
    ('Stiff',                        'gluteos'),
    ('Passada (Lunge)',              'gluteos'),
    ('Elevação Pélvica',             'gluteos'),
    -- Quadríceps
    ('Leg Press',                    'quadriceps'),
    ('Extensora',                    'quadriceps'),
    ('Agachamento Hack',             'quadriceps'),
    -- Posterior de coxa
    ('Flexora',                      'posterior'),
    ('Mesa Flexora',                 'posterior'),
    -- Panturrilha
    ('Panturrilha em Pé',            'panturrilha'),
    ('Panturrilha Sentado',          'panturrilha'),
    -- Cardio
    ('Esteira',                      'cardio'),
    ('Bicicleta Ergométrica',        'cardio'),
    ('Elíptico',                     'cardio'),
    ('Corda',                        'cardio');


-- EXEMPLO DE ALUNO (para testes)

INSERT OR IGNORE INTO alunos_aluno
    (nome, email, telefone, sexo, cidade, estado, objetivo, ativo)
VALUES
    ('Maria Silva',  'maria@email.com',  '(11) 91111-1111', 'F',
     'Mogi das Cruzes', 'SP', 'Emagrecimento e condicionamento físico', 1),
    ('João Santos',  'joao@email.com',   '(11) 92222-2222', 'M',
     'Mogi das Cruzes', 'SP', 'Hipertrofia muscular', 1),
    ('Ana Oliveira', 'ana@email.com',    '(11) 93333-3333', 'F',
     'Mogi das Cruzes', 'SP', 'Definição muscular e saúde', 1);


