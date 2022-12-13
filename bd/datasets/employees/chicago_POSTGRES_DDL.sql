CREATE TABLE public.chicago (
	nome varchar(50) NULL DEFAULT NULL::character varying,
	cargo varchar(50) NULL DEFAULT NULL::character varying,
	departamento varchar(50) NULL DEFAULT NULL::character varying,
	full_ou_part varchar(50) NULL DEFAULT NULL::character varying,
	salario_ou_hora varchar(50) NULL DEFAULT NULL::character varying,
	horas_tipicas int4 NULL,
	salario_anual float8 NULL,
	valor_hora float8 NULL
);
