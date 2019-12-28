--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.19
-- Dumped by pg_dump version 9.5.19

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: blog
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO blog;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: blog
--

CREATE SEQUENCE public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO blog;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: blog
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: blog
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO blog;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: blog
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO blog;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: blog
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: blog
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO blog;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: blog
--

CREATE SEQUENCE public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO blog;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: blog
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: blog
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO blog;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: blog
--

CREATE TABLE public.auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO blog;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: blog
--

CREATE SEQUENCE public.auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO blog;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: blog
--

ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: blog
--

CREATE SEQUENCE public.auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO blog;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: blog
--

ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: blog
--

CREATE TABLE public.auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO blog;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: blog
--

CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO blog;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: blog
--

ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;


--
-- Name: blog_article; Type: TABLE; Schema: public; Owner: blog
--

CREATE TABLE public.blog_article (
    id integer NOT NULL,
    title character varying(200) NOT NULL,
    date_time date NOT NULL,
    content text,
    digest text,
    view bigint NOT NULL,
    comment bigint NOT NULL,
    picture character varying(200) NOT NULL,
    author_id integer NOT NULL,
    category_id integer NOT NULL
);


ALTER TABLE public.blog_article OWNER TO blog;

--
-- Name: blog_article_id_seq; Type: SEQUENCE; Schema: public; Owner: blog
--

CREATE SEQUENCE public.blog_article_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.blog_article_id_seq OWNER TO blog;

--
-- Name: blog_article_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: blog
--

ALTER SEQUENCE public.blog_article_id_seq OWNED BY public.blog_article.id;


--
-- Name: blog_article_tag; Type: TABLE; Schema: public; Owner: blog
--

CREATE TABLE public.blog_article_tag (
    id integer NOT NULL,
    article_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE public.blog_article_tag OWNER TO blog;

--
-- Name: blog_article_tag_id_seq; Type: SEQUENCE; Schema: public; Owner: blog
--

CREATE SEQUENCE public.blog_article_tag_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.blog_article_tag_id_seq OWNER TO blog;

--
-- Name: blog_article_tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: blog
--

ALTER SEQUENCE public.blog_article_tag_id_seq OWNED BY public.blog_article_tag.id;


--
-- Name: blog_category; Type: TABLE; Schema: public; Owner: blog
--

CREATE TABLE public.blog_category (
    id integer NOT NULL,
    name character varying(30) NOT NULL,
    created_time timestamp with time zone NOT NULL,
    last_mod_time timestamp with time zone NOT NULL
);


ALTER TABLE public.blog_category OWNER TO blog;

--
-- Name: blog_category_id_seq; Type: SEQUENCE; Schema: public; Owner: blog
--

CREATE SEQUENCE public.blog_category_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.blog_category_id_seq OWNER TO blog;

--
-- Name: blog_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: blog
--

ALTER SEQUENCE public.blog_category_id_seq OWNED BY public.blog_category.id;


--
-- Name: blog_comment; Type: TABLE; Schema: public; Owner: blog
--

CREATE TABLE public.blog_comment (
    id integer NOT NULL,
    title character varying(100) NOT NULL,
    source_id character varying(25) NOT NULL,
    create_time timestamp with time zone NOT NULL,
    user_name character varying(25) NOT NULL,
    url character varying(100) NOT NULL,
    comment character varying(500) NOT NULL
);


ALTER TABLE public.blog_comment OWNER TO blog;

--
-- Name: blog_comment_id_seq; Type: SEQUENCE; Schema: public; Owner: blog
--

CREATE SEQUENCE public.blog_comment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.blog_comment_id_seq OWNER TO blog;

--
-- Name: blog_comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: blog
--

ALTER SEQUENCE public.blog_comment_id_seq OWNED BY public.blog_comment.id;


--
-- Name: blog_tag; Type: TABLE; Schema: public; Owner: blog
--

CREATE TABLE public.blog_tag (
    id integer NOT NULL,
    tag_name character varying(30) NOT NULL
);


ALTER TABLE public.blog_tag OWNER TO blog;

--
-- Name: blog_tag_id_seq; Type: SEQUENCE; Schema: public; Owner: blog
--

CREATE SEQUENCE public.blog_tag_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.blog_tag_id_seq OWNER TO blog;

--
-- Name: blog_tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: blog
--

ALTER SEQUENCE public.blog_tag_id_seq OWNED BY public.blog_tag.id;


--
-- Name: blog_userprofile; Type: TABLE; Schema: public; Owner: blog
--

CREATE TABLE public.blog_userprofile (
    id integer NOT NULL,
    info character varying(256) NOT NULL,
    detail jsonb NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.blog_userprofile OWNER TO blog;

--
-- Name: blog_userprofile_id_seq; Type: SEQUENCE; Schema: public; Owner: blog
--

CREATE SEQUENCE public.blog_userprofile_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.blog_userprofile_id_seq OWNER TO blog;

--
-- Name: blog_userprofile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: blog
--

ALTER SEQUENCE public.blog_userprofile_id_seq OWNED BY public.blog_userprofile.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: blog
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO blog;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: blog
--

CREATE SEQUENCE public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO blog;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: blog
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: blog
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO blog;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: blog
--

CREATE SEQUENCE public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO blog;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: blog
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: blog
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO blog;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: blog
--

CREATE SEQUENCE public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO blog;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: blog
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: blog
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO blog;

--
-- Name: id; Type: DEFAULT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.blog_article ALTER COLUMN id SET DEFAULT nextval('public.blog_article_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.blog_article_tag ALTER COLUMN id SET DEFAULT nextval('public.blog_article_tag_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.blog_category ALTER COLUMN id SET DEFAULT nextval('public.blog_category_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.blog_comment ALTER COLUMN id SET DEFAULT nextval('public.blog_comment_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.blog_tag ALTER COLUMN id SET DEFAULT nextval('public.blog_tag_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.blog_userprofile ALTER COLUMN id SET DEFAULT nextval('public.blog_userprofile_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: blog
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: blog
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: blog
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: blog
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: blog
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can add permission	2	add_permission
5	Can change permission	2	change_permission
6	Can delete permission	2	delete_permission
7	Can add user	3	add_user
8	Can change user	3	change_user
9	Can delete user	3	delete_user
10	Can add group	4	add_group
11	Can change group	4	change_group
12	Can delete group	4	delete_group
13	Can add content type	5	add_contenttype
14	Can change content type	5	change_contenttype
15	Can delete content type	5	delete_contenttype
16	Can add session	6	add_session
17	Can change session	6	change_session
18	Can delete session	6	delete_session
19	Can add comment	7	add_comment
20	Can change comment	7	change_comment
21	Can delete comment	7	delete_comment
22	Can add user profile	8	add_userprofile
23	Can change user profile	8	change_userprofile
24	Can delete user profile	8	delete_userprofile
25	Can add 文章类型	9	add_category
26	Can change 文章类型	9	change_category
27	Can delete 文章类型	9	delete_category
28	Can add article	10	add_article
29	Can change article	10	change_article
30	Can delete article	10	delete_article
31	Can add tag	11	add_tag
32	Can change tag	11	change_tag
33	Can delete tag	11	delete_tag
\.


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: blog
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 33, true);


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: blog
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$30000$y4EotExnLW76$IG4ICB9uVJyORy+cxLt3WhDUrVMsvtUGuTkaJIAYwws=	2019-09-09 12:13:48.277063+00	t	root				t	t	2019-09-09 11:10:24.066898+00
2	pbkdf2_sha256$30000$J2ZlRJ4jdGkd$edXTepm1KCsgVNi0hYvHwvfMzTT9XXcC+0eCQ3pEOx8=	\N	t	blog				t	t	2019-09-09 11:12:00+00
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: blog
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: blog
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: blog
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 2, true);


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: blog
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: blog
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Data for Name: blog_article; Type: TABLE DATA; Schema: public; Owner: blog
--

COPY public.blog_article (id, title, date_time, content, digest, view, comment, picture, author_id, category_id) FROM stdin;
\.


--
-- Name: blog_article_id_seq; Type: SEQUENCE SET; Schema: public; Owner: blog
--

SELECT pg_catalog.setval('public.blog_article_id_seq', 1, false);


--
-- Data for Name: blog_article_tag; Type: TABLE DATA; Schema: public; Owner: blog
--

COPY public.blog_article_tag (id, article_id, tag_id) FROM stdin;
\.


--
-- Name: blog_article_tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: blog
--

SELECT pg_catalog.setval('public.blog_article_tag_id_seq', 1, false);


--
-- Data for Name: blog_category; Type: TABLE DATA; Schema: public; Owner: blog
--

COPY public.blog_category (id, name, created_time, last_mod_time) FROM stdin;
\.


--
-- Name: blog_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: blog
--

SELECT pg_catalog.setval('public.blog_category_id_seq', 1, false);


--
-- Data for Name: blog_comment; Type: TABLE DATA; Schema: public; Owner: blog
--

COPY public.blog_comment (id, title, source_id, create_time, user_name, url, comment) FROM stdin;
\.


--
-- Name: blog_comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: blog
--

SELECT pg_catalog.setval('public.blog_comment_id_seq', 1, false);


--
-- Data for Name: blog_tag; Type: TABLE DATA; Schema: public; Owner: blog
--

COPY public.blog_tag (id, tag_name) FROM stdin;
\.


--
-- Name: blog_tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: blog
--

SELECT pg_catalog.setval('public.blog_tag_id_seq', 1, false);


--
-- Data for Name: blog_userprofile; Type: TABLE DATA; Schema: public; Owner: blog
--

COPY public.blog_userprofile (id, info, detail, user_id) FROM stdin;
1	flag{no_delete}	{"test": "test"}	2
\.


--
-- Name: blog_userprofile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: blog
--

SELECT pg_catalog.setval('public.blog_userprofile_id_seq', 1, true);


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: blog
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2019-09-09 11:12:54.977083+00	2	blog	1	[{"added": {}}]	3	1
2	2019-09-09 11:15:31.371951+00	1	UserProfile object	1	[{"added": {}}]	8	1
3	2019-09-09 11:23:14.565983+00	2	blog	2	[{"changed": {"fields": ["is_staff"]}}]	3	1
4	2019-09-09 12:15:32.981792+00	2	blog	2	[{"changed": {"fields": ["is_superuser"]}}]	3	1
5	2019-09-09 12:16:17.970668+00	1	UserProfile object	2	[{"changed": {"fields": ["info"]}}]	8	1
\.


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: blog
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 5, true);


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: blog
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	user
4	auth	group
5	contenttypes	contenttype
6	sessions	session
7	blog	comment
8	blog	userprofile
9	blog	category
10	blog	article
11	blog	tag
\.


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: blog
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 11, true);


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: blog
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2019-09-09 11:05:36.965391+00
2	auth	0001_initial	2019-09-09 11:05:38.083547+00
3	admin	0001_initial	2019-09-09 11:05:38.568171+00
4	admin	0002_logentry_remove_auto_add	2019-09-09 11:05:38.871648+00
5	contenttypes	0002_remove_content_type_name	2019-09-09 11:05:39.68663+00
6	auth	0002_alter_permission_name_max_length	2019-09-09 11:05:40.066865+00
7	auth	0003_alter_user_email_max_length	2019-09-09 11:05:40.383622+00
8	auth	0004_alter_user_username_opts	2019-09-09 11:05:40.666956+00
9	auth	0005_alter_user_last_login_null	2019-09-09 11:05:40.97474+00
10	auth	0006_require_contenttypes_0002	2019-09-09 11:05:40.980242+00
11	auth	0007_alter_validators_add_error_messages	2019-09-09 11:05:41.273122+00
12	auth	0008_alter_user_username_max_length	2019-09-09 11:05:41.571053+00
13	blog	0001_initial	2019-09-09 11:05:43.871672+00
14	blog	0002_userprofile	2019-09-09 11:05:44.368201+00
15	sessions	0001_initial	2019-09-09 11:05:44.568985+00
\.


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: blog
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 15, true);


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: blog
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions_group_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission_content_type_id_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_user_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_user_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: blog_article_pkey; Type: CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.blog_article
    ADD CONSTRAINT blog_article_pkey PRIMARY KEY (id);


--
-- Name: blog_article_tag_article_id_818e752b_uniq; Type: CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.blog_article_tag
    ADD CONSTRAINT blog_article_tag_article_id_818e752b_uniq UNIQUE (article_id, tag_id);


--
-- Name: blog_article_tag_pkey; Type: CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.blog_article_tag
    ADD CONSTRAINT blog_article_tag_pkey PRIMARY KEY (id);


--
-- Name: blog_category_pkey; Type: CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.blog_category
    ADD CONSTRAINT blog_category_pkey PRIMARY KEY (id);


--
-- Name: blog_comment_pkey; Type: CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.blog_comment
    ADD CONSTRAINT blog_comment_pkey PRIMARY KEY (id);


--
-- Name: blog_tag_pkey; Type: CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.blog_tag
    ADD CONSTRAINT blog_tag_pkey PRIMARY KEY (id);


--
-- Name: blog_userprofile_pkey; Type: CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.blog_userprofile
    ADD CONSTRAINT blog_userprofile_pkey PRIMARY KEY (id);


--
-- Name: blog_userprofile_user_id_key; Type: CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.blog_userprofile
    ADD CONSTRAINT blog_userprofile_user_id_key UNIQUE (user_id);


--
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type_app_label_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: blog
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_0e939a4f; Type: INDEX; Schema: public; Owner: blog
--

CREATE INDEX auth_group_permissions_0e939a4f ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_8373b171; Type: INDEX; Schema: public; Owner: blog
--

CREATE INDEX auth_group_permissions_8373b171 ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_417f1b1c; Type: INDEX; Schema: public; Owner: blog
--

CREATE INDEX auth_permission_417f1b1c ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_0e939a4f; Type: INDEX; Schema: public; Owner: blog
--

CREATE INDEX auth_user_groups_0e939a4f ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_e8701ad4; Type: INDEX; Schema: public; Owner: blog
--

CREATE INDEX auth_user_groups_e8701ad4 ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_8373b171; Type: INDEX; Schema: public; Owner: blog
--

CREATE INDEX auth_user_user_permissions_8373b171 ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_e8701ad4; Type: INDEX; Schema: public; Owner: blog
--

CREATE INDEX auth_user_user_permissions_e8701ad4 ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: blog
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: blog_article_4f331e2f; Type: INDEX; Schema: public; Owner: blog
--

CREATE INDEX blog_article_4f331e2f ON public.blog_article USING btree (author_id);


--
-- Name: blog_article_b583a629; Type: INDEX; Schema: public; Owner: blog
--

CREATE INDEX blog_article_b583a629 ON public.blog_article USING btree (category_id);


--
-- Name: blog_article_tag_76f094bc; Type: INDEX; Schema: public; Owner: blog
--

CREATE INDEX blog_article_tag_76f094bc ON public.blog_article_tag USING btree (tag_id);


--
-- Name: blog_article_tag_a00c1b00; Type: INDEX; Schema: public; Owner: blog
--

CREATE INDEX blog_article_tag_a00c1b00 ON public.blog_article_tag USING btree (article_id);


--
-- Name: django_admin_log_417f1b1c; Type: INDEX; Schema: public; Owner: blog
--

CREATE INDEX django_admin_log_417f1b1c ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_e8701ad4; Type: INDEX; Schema: public; Owner: blog
--

CREATE INDEX django_admin_log_e8701ad4 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_de54fa62; Type: INDEX; Schema: public; Owner: blog
--

CREATE INDEX django_session_de54fa62 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: blog
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: auth_group_permiss_permission_id_84c5c92e_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permiss_permission_id_84c5c92e_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permiss_content_type_id_2f476e4b_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permiss_content_type_id_2f476e4b_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_per_permission_id_1fbb5f2c_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_per_permission_id_1fbb5f2c_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: blog_article_author_id_905add38_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.blog_article
    ADD CONSTRAINT blog_article_author_id_905add38_fk_auth_user_id FOREIGN KEY (author_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: blog_article_category_id_7e38f15e_fk_blog_category_id; Type: FK CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.blog_article
    ADD CONSTRAINT blog_article_category_id_7e38f15e_fk_blog_category_id FOREIGN KEY (category_id) REFERENCES public.blog_category(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: blog_article_tag_article_id_8db2395e_fk_blog_article_id; Type: FK CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.blog_article_tag
    ADD CONSTRAINT blog_article_tag_article_id_8db2395e_fk_blog_article_id FOREIGN KEY (article_id) REFERENCES public.blog_article(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: blog_article_tag_tag_id_f2afe66b_fk_blog_tag_id; Type: FK CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.blog_article_tag
    ADD CONSTRAINT blog_article_tag_tag_id_f2afe66b_fk_blog_tag_id FOREIGN KEY (tag_id) REFERENCES public.blog_tag(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: blog_userprofile_user_id_dfc03473_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.blog_userprofile
    ADD CONSTRAINT blog_userprofile_user_id_dfc03473_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_content_type_id_c4bce8eb_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_content_type_id_c4bce8eb_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: blog
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

