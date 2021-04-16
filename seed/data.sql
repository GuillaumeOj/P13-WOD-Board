--
-- PostgreSQL database dump
--

-- Dumped from database version 13.2 (Ubuntu 13.2-1.pgdg20.10+1)
-- Dumped by pg_dump version 13.2 (Ubuntu 13.2-1.pgdg20.10+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: guillaume
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO guillaume;

--
-- Name: equipment; Type: TABLE; Schema: public; Owner: guillaume
--

CREATE TABLE public.equipment (
    id integer NOT NULL,
    name character varying(250) NOT NULL,
    unit_id integer
);


ALTER TABLE public.equipment OWNER TO guillaume;

--
-- Name: equipment_id_seq; Type: SEQUENCE; Schema: public; Owner: guillaume
--

CREATE SEQUENCE public.equipment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.equipment_id_seq OWNER TO guillaume;

--
-- Name: equipment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: guillaume
--

ALTER SEQUENCE public.equipment_id_seq OWNED BY public.equipment.id;


--
-- Name: movement; Type: TABLE; Schema: public; Owner: guillaume
--

CREATE TABLE public.movement (
    id integer NOT NULL,
    name character varying(250) NOT NULL,
    unit_id integer
);


ALTER TABLE public.movement OWNER TO guillaume;

--
-- Name: movement_equipment; Type: TABLE; Schema: public; Owner: guillaume
--

CREATE TABLE public.movement_equipment (
    id integer NOT NULL,
    movement_id integer,
    equipment_id integer
);


ALTER TABLE public.movement_equipment OWNER TO guillaume;

--
-- Name: movement_equipment_id_seq; Type: SEQUENCE; Schema: public; Owner: guillaume
--

CREATE SEQUENCE public.movement_equipment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.movement_equipment_id_seq OWNER TO guillaume;

--
-- Name: movement_equipment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: guillaume
--

ALTER SEQUENCE public.movement_equipment_id_seq OWNED BY public.movement_equipment.id;


--
-- Name: movement_goal; Type: TABLE; Schema: public; Owner: guillaume
--

CREATE TABLE public.movement_goal (
    id integer NOT NULL,
    movement_id integer,
    repetition integer
);


ALTER TABLE public.movement_goal OWNER TO guillaume;

--
-- Name: movement_goal_equipment; Type: TABLE; Schema: public; Owner: guillaume
--

CREATE TABLE public.movement_goal_equipment (
    id integer NOT NULL,
    movement_goal_id integer,
    equipment_id integer
);


ALTER TABLE public.movement_goal_equipment OWNER TO guillaume;

--
-- Name: movement_goal_equipment_id_seq; Type: SEQUENCE; Schema: public; Owner: guillaume
--

CREATE SEQUENCE public.movement_goal_equipment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.movement_goal_equipment_id_seq OWNER TO guillaume;

--
-- Name: movement_goal_equipment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: guillaume
--

ALTER SEQUENCE public.movement_goal_equipment_id_seq OWNED BY public.movement_goal_equipment.id;


--
-- Name: movement_goal_id_seq; Type: SEQUENCE; Schema: public; Owner: guillaume
--

CREATE SEQUENCE public.movement_goal_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.movement_goal_id_seq OWNER TO guillaume;

--
-- Name: movement_goal_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: guillaume
--

ALTER SEQUENCE public.movement_goal_id_seq OWNED BY public.movement_goal.id;


--
-- Name: movement_id_seq; Type: SEQUENCE; Schema: public; Owner: guillaume
--

CREATE SEQUENCE public.movement_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.movement_id_seq OWNER TO guillaume;

--
-- Name: movement_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: guillaume
--

ALTER SEQUENCE public.movement_id_seq OWNED BY public.movement.id;


--
-- Name: round; Type: TABLE; Schema: public; Owner: guillaume
--

CREATE TABLE public.round (
    id integer NOT NULL,
    "position" integer NOT NULL,
    duration_seconds integer,
    wod_id integer,
    parent_id integer
);


ALTER TABLE public.round OWNER TO guillaume;

--
-- Name: round_id_seq; Type: SEQUENCE; Schema: public; Owner: guillaume
--

CREATE SEQUENCE public.round_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.round_id_seq OWNER TO guillaume;

--
-- Name: round_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: guillaume
--

ALTER SEQUENCE public.round_id_seq OWNED BY public.round.id;


--
-- Name: round_movement_goal; Type: TABLE; Schema: public; Owner: guillaume
--

CREATE TABLE public.round_movement_goal (
    id integer NOT NULL,
    round_id integer,
    movement_goal_id integer
);


ALTER TABLE public.round_movement_goal OWNER TO guillaume;

--
-- Name: round_movement_goal_id_seq; Type: SEQUENCE; Schema: public; Owner: guillaume
--

CREATE SEQUENCE public.round_movement_goal_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.round_movement_goal_id_seq OWNER TO guillaume;

--
-- Name: round_movement_goal_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: guillaume
--

ALTER SEQUENCE public.round_movement_goal_id_seq OWNED BY public.round_movement_goal.id;


--
-- Name: unit; Type: TABLE; Schema: public; Owner: guillaume
--

CREATE TABLE public.unit (
    id integer NOT NULL,
    name character varying(250) NOT NULL,
    symbol character varying(5) NOT NULL
);


ALTER TABLE public.unit OWNER TO guillaume;

--
-- Name: unit_id_seq; Type: SEQUENCE; Schema: public; Owner: guillaume
--

CREATE SEQUENCE public.unit_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.unit_id_seq OWNER TO guillaume;

--
-- Name: unit_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: guillaume
--

ALTER SEQUENCE public.unit_id_seq OWNED BY public.unit.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: guillaume
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    email character varying NOT NULL,
    hashed_password character varying NOT NULL,
    username character varying NOT NULL,
    first_name character varying,
    last_name character varying
);


ALTER TABLE public."user" OWNER TO guillaume;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: guillaume
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_id_seq OWNER TO guillaume;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: guillaume
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: wod; Type: TABLE; Schema: public; Owner: guillaume
--

CREATE TABLE public.wod (
    id integer NOT NULL,
    description character varying,
    note character varying,
    date timestamp without time zone DEFAULT now() NOT NULL,
    wod_type_id integer
);


ALTER TABLE public.wod OWNER TO guillaume;

--
-- Name: wod_id_seq; Type: SEQUENCE; Schema: public; Owner: guillaume
--

CREATE SEQUENCE public.wod_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.wod_id_seq OWNER TO guillaume;

--
-- Name: wod_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: guillaume
--

ALTER SEQUENCE public.wod_id_seq OWNED BY public.wod.id;


--
-- Name: wod_type; Type: TABLE; Schema: public; Owner: guillaume
--

CREATE TABLE public.wod_type (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.wod_type OWNER TO guillaume;

--
-- Name: wod_type_id_seq; Type: SEQUENCE; Schema: public; Owner: guillaume
--

CREATE SEQUENCE public.wod_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.wod_type_id_seq OWNER TO guillaume;

--
-- Name: wod_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: guillaume
--

ALTER SEQUENCE public.wod_type_id_seq OWNED BY public.wod_type.id;


--
-- Name: equipment id; Type: DEFAULT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.equipment ALTER COLUMN id SET DEFAULT nextval('public.equipment_id_seq'::regclass);


--
-- Name: movement id; Type: DEFAULT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.movement ALTER COLUMN id SET DEFAULT nextval('public.movement_id_seq'::regclass);


--
-- Name: movement_equipment id; Type: DEFAULT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.movement_equipment ALTER COLUMN id SET DEFAULT nextval('public.movement_equipment_id_seq'::regclass);


--
-- Name: movement_goal id; Type: DEFAULT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.movement_goal ALTER COLUMN id SET DEFAULT nextval('public.movement_goal_id_seq'::regclass);


--
-- Name: movement_goal_equipment id; Type: DEFAULT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.movement_goal_equipment ALTER COLUMN id SET DEFAULT nextval('public.movement_goal_equipment_id_seq'::regclass);


--
-- Name: round id; Type: DEFAULT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.round ALTER COLUMN id SET DEFAULT nextval('public.round_id_seq'::regclass);


--
-- Name: round_movement_goal id; Type: DEFAULT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.round_movement_goal ALTER COLUMN id SET DEFAULT nextval('public.round_movement_goal_id_seq'::regclass);


--
-- Name: unit id; Type: DEFAULT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.unit ALTER COLUMN id SET DEFAULT nextval('public.unit_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Name: wod id; Type: DEFAULT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.wod ALTER COLUMN id SET DEFAULT nextval('public.wod_id_seq'::regclass);


--
-- Name: wod_type id; Type: DEFAULT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.wod_type ALTER COLUMN id SET DEFAULT nextval('public.wod_type_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: guillaume
--

COPY public.alembic_version (version_num) FROM stdin;
865d47baf506
\.


--
-- Data for Name: equipment; Type: TABLE DATA; Schema: public; Owner: guillaume
--

COPY public.equipment (id, name, unit_id) FROM stdin;
1	Dumbbell	2
2	Kettelbell	2
3	Weight Vest	2
4	Pull-Up Bar	\N
5	Gymnatic Rows	\N
6	Box	\N
\.


--
-- Data for Name: movement; Type: TABLE DATA; Schema: public; Owner: guillaume
--

COPY public.movement (id, name, unit_id) FROM stdin;
2	Devil Press	1
3	Pull-Up	1
4	Push-Up	1
5	Air Squats	1
6	Run	4
7	Ring Rows	1
8	One Arm Bent Over Row	1
9	Incline Push-Up	1
10	Knee Push-Up	1
11	Jumping Pull-Up	1
\.


--
-- Data for Name: movement_equipment; Type: TABLE DATA; Schema: public; Owner: guillaume
--

COPY public.movement_equipment (id, movement_id, equipment_id) FROM stdin;
1	2	1
2	2	2
4	4	3
5	5	3
6	6	3
7	7	5
8	8	1
9	8	2
3	3	4
10	9	6
11	11	4
12	7	3
\.


--
-- Data for Name: movement_goal; Type: TABLE DATA; Schema: public; Owner: guillaume
--

COPY public.movement_goal (id, movement_id, repetition) FROM stdin;
1	3	5
2	4	10
3	5	15
4	6	1000
5	3	100
6	4	200
7	5	300
8	6	1000
\.


--
-- Data for Name: movement_goal_equipment; Type: TABLE DATA; Schema: public; Owner: guillaume
--

COPY public.movement_goal_equipment (id, movement_goal_id, equipment_id) FROM stdin;
1	1	4
2	4	3
3	5	3
4	6	3
5	7	3
6	8	3
7	5	4
\.


--
-- Data for Name: round; Type: TABLE DATA; Schema: public; Owner: guillaume
--

COPY public.round (id, "position", duration_seconds, wod_id, parent_id) FROM stdin;
2	1	1200	1	\N
3	1	\N	2	\N
4	1	1800	3	\N
\.


--
-- Data for Name: round_movement_goal; Type: TABLE DATA; Schema: public; Owner: guillaume
--

COPY public.round_movement_goal (id, round_id, movement_goal_id) FROM stdin;
1	2	1
2	2	2
3	2	3
4	3	4
5	3	5
6	3	6
7	3	7
8	3	8
\.


--
-- Data for Name: unit; Type: TABLE DATA; Schema: public; Owner: guillaume
--

COPY public.unit (id, name, symbol) FROM stdin;
1	Unit	u
2	Kilogram	kg
3	Load\n	L
4	Meter	m
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: guillaume
--

COPY public."user" (id, email, hashed_password, username, first_name, last_name) FROM stdin;
1	guillaume@ojardias.me	$2b$12$yawHZXN3WDzAfdusw2OXquDhAkKdxbZEWPWxuA5CX7SVaXnnXpsau	GuillaumeOj	\N	\N
2	foo@bar.com	$2b$12$/fXBp9vvg08McLOWqyL3JeaEfQ1entnXoZ66fckz5dQ13.Bnv1x92	foo-bar	\N	\N
3	guillaume@bar.com	$2b$12$Gj6EdUICuwsX8xNPYkgsg.uGNwAGpHZrFqEuwB.7ntW4zYyep4WWi	guillaume-bar	\N	\N
\.


--
-- Data for Name: wod; Type: TABLE DATA; Schema: public; Owner: guillaume
--

COPY public.wod (id, description, note, date, wod_type_id) FROM stdin;
2	Benchmark Murph	Murph Day!	2021-04-16 00:00:00	2
3	Benchmark Chelsea	\N	2021-04-17 00:00:00	4
1	Benchmark Cindy	\N	2021-04-15 00:00:00	1
\.


--
-- Data for Name: wod_type; Type: TABLE DATA; Schema: public; Owner: guillaume
--

COPY public.wod_type (id, name) FROM stdin;
1	AMRAP
2	For Time
3	Tabata
4	EMOM
5	For Load
\.


--
-- Name: equipment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: guillaume
--

SELECT pg_catalog.setval('public.equipment_id_seq', 6, true);


--
-- Name: movement_equipment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: guillaume
--

SELECT pg_catalog.setval('public.movement_equipment_id_seq', 12, true);


--
-- Name: movement_goal_equipment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: guillaume
--

SELECT pg_catalog.setval('public.movement_goal_equipment_id_seq', 7, true);


--
-- Name: movement_goal_id_seq; Type: SEQUENCE SET; Schema: public; Owner: guillaume
--

SELECT pg_catalog.setval('public.movement_goal_id_seq', 8, true);


--
-- Name: movement_id_seq; Type: SEQUENCE SET; Schema: public; Owner: guillaume
--

SELECT pg_catalog.setval('public.movement_id_seq', 11, true);


--
-- Name: round_id_seq; Type: SEQUENCE SET; Schema: public; Owner: guillaume
--

SELECT pg_catalog.setval('public.round_id_seq', 3, true);


--
-- Name: round_movement_goal_id_seq; Type: SEQUENCE SET; Schema: public; Owner: guillaume
--

SELECT pg_catalog.setval('public.round_movement_goal_id_seq', 8, true);


--
-- Name: unit_id_seq; Type: SEQUENCE SET; Schema: public; Owner: guillaume
--

SELECT pg_catalog.setval('public.unit_id_seq', 3, true);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: guillaume
--

SELECT pg_catalog.setval('public.user_id_seq', 3, true);


--
-- Name: wod_id_seq; Type: SEQUENCE SET; Schema: public; Owner: guillaume
--

SELECT pg_catalog.setval('public.wod_id_seq', 3, true);


--
-- Name: wod_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: guillaume
--

SELECT pg_catalog.setval('public.wod_type_id_seq', 5, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: equipment equipment_name_key; Type: CONSTRAINT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.equipment
    ADD CONSTRAINT equipment_name_key UNIQUE (name);


--
-- Name: equipment equipment_pkey; Type: CONSTRAINT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.equipment
    ADD CONSTRAINT equipment_pkey PRIMARY KEY (id);


--
-- Name: movement_equipment movement_equipment_pkey; Type: CONSTRAINT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.movement_equipment
    ADD CONSTRAINT movement_equipment_pkey PRIMARY KEY (id);


--
-- Name: movement_goal_equipment movement_goal_equipment_pkey; Type: CONSTRAINT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.movement_goal_equipment
    ADD CONSTRAINT movement_goal_equipment_pkey PRIMARY KEY (id);


--
-- Name: movement_goal movement_goal_pkey; Type: CONSTRAINT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.movement_goal
    ADD CONSTRAINT movement_goal_pkey PRIMARY KEY (id);


--
-- Name: movement movement_name_key; Type: CONSTRAINT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.movement
    ADD CONSTRAINT movement_name_key UNIQUE (name);


--
-- Name: movement movement_pkey; Type: CONSTRAINT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.movement
    ADD CONSTRAINT movement_pkey PRIMARY KEY (id);


--
-- Name: unit name_symbol; Type: CONSTRAINT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.unit
    ADD CONSTRAINT name_symbol UNIQUE (name, symbol);


--
-- Name: round_movement_goal round_movement_goal_pkey; Type: CONSTRAINT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.round_movement_goal
    ADD CONSTRAINT round_movement_goal_pkey PRIMARY KEY (id);


--
-- Name: round round_pkey; Type: CONSTRAINT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.round
    ADD CONSTRAINT round_pkey PRIMARY KEY (id);


--
-- Name: unit unit_name_key; Type: CONSTRAINT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.unit
    ADD CONSTRAINT unit_name_key UNIQUE (name);


--
-- Name: unit unit_pkey; Type: CONSTRAINT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.unit
    ADD CONSTRAINT unit_pkey PRIMARY KEY (id);


--
-- Name: user user_email_key; Type: CONSTRAINT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_email_key UNIQUE (email);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: user user_username_key; Type: CONSTRAINT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_username_key UNIQUE (username);


--
-- Name: round wod_id_position; Type: CONSTRAINT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.round
    ADD CONSTRAINT wod_id_position UNIQUE (wod_id, "position");


--
-- Name: wod wod_pkey; Type: CONSTRAINT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.wod
    ADD CONSTRAINT wod_pkey PRIMARY KEY (id);


--
-- Name: wod_type wod_type_name_key; Type: CONSTRAINT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.wod_type
    ADD CONSTRAINT wod_type_name_key UNIQUE (name);


--
-- Name: wod_type wod_type_pkey; Type: CONSTRAINT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.wod_type
    ADD CONSTRAINT wod_type_pkey PRIMARY KEY (id);


--
-- Name: equipment equipment_unit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.equipment
    ADD CONSTRAINT equipment_unit_id_fkey FOREIGN KEY (unit_id) REFERENCES public.unit(id);


--
-- Name: movement_equipment movement_equipment_equipment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.movement_equipment
    ADD CONSTRAINT movement_equipment_equipment_id_fkey FOREIGN KEY (equipment_id) REFERENCES public.equipment(id);


--
-- Name: movement_equipment movement_equipment_movement_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.movement_equipment
    ADD CONSTRAINT movement_equipment_movement_id_fkey FOREIGN KEY (movement_id) REFERENCES public.movement(id);


--
-- Name: movement_goal_equipment movement_goal_equipment_equipment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.movement_goal_equipment
    ADD CONSTRAINT movement_goal_equipment_equipment_id_fkey FOREIGN KEY (equipment_id) REFERENCES public.equipment(id);


--
-- Name: movement_goal_equipment movement_goal_equipment_movement_goal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.movement_goal_equipment
    ADD CONSTRAINT movement_goal_equipment_movement_goal_id_fkey FOREIGN KEY (movement_goal_id) REFERENCES public.movement_goal(id);


--
-- Name: movement_goal movement_goal_movement_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.movement_goal
    ADD CONSTRAINT movement_goal_movement_id_fkey FOREIGN KEY (movement_id) REFERENCES public.movement(id);


--
-- Name: movement movement_unit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.movement
    ADD CONSTRAINT movement_unit_id_fkey FOREIGN KEY (unit_id) REFERENCES public.unit(id);


--
-- Name: round_movement_goal round_movement_goal_movement_goal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.round_movement_goal
    ADD CONSTRAINT round_movement_goal_movement_goal_id_fkey FOREIGN KEY (movement_goal_id) REFERENCES public.movement_goal(id);


--
-- Name: round_movement_goal round_movement_goal_round_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.round_movement_goal
    ADD CONSTRAINT round_movement_goal_round_id_fkey FOREIGN KEY (round_id) REFERENCES public.round(id);


--
-- Name: round round_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.round
    ADD CONSTRAINT round_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.round(id);


--
-- Name: round round_wod_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.round
    ADD CONSTRAINT round_wod_id_fkey FOREIGN KEY (wod_id) REFERENCES public.wod(id);


--
-- Name: wod wod_wod_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: guillaume
--

ALTER TABLE ONLY public.wod
    ADD CONSTRAINT wod_wod_type_id_fkey FOREIGN KEY (wod_type_id) REFERENCES public.wod_type(id);


--
-- PostgreSQL database dump complete
--

