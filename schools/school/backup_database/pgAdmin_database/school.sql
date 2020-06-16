PGDMP     :                    x            school     12.1 (Ubuntu 12.1-1.pgdg18.04+1)     12.1 (Ubuntu 12.1-1.pgdg18.04+1) *    y           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            z           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            {           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            |           1262    1110480    school    DATABASE     n   CREATE DATABASE school WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'C' LC_CTYPE = 'fr_FR.UTF-8';
    DROP DATABASE school;
                odoo    false            ;           1259    1110872    account_move    TABLE       CREATE TABLE public.account_move (
    id integer NOT NULL,
    name character varying NOT NULL,
    ref character varying,
    date date NOT NULL,
    journal_id integer NOT NULL,
    currency_id integer,
    state character varying NOT NULL,
    partner_id integer,
    amount numeric,
    narration text,
    company_id integer,
    matched_percentage numeric,
    tax_cash_basis_rec_id integer,
    auto_reverse boolean,
    reverse_date date,
    reverse_entry_id integer,
    create_uid integer,
    create_date timestamp without time zone,
    write_uid integer,
    write_date timestamp without time zone,
    stock_move_id integer
);
     DROP TABLE public.account_move;
       public         heap    odoo    false            }           0    0    TABLE account_move    COMMENT     ;   COMMENT ON TABLE public.account_move IS 'Journal Entries';
          public          odoo    false    315            ~           0    0    COLUMN account_move.name    COMMENT     8   COMMENT ON COLUMN public.account_move.name IS 'Number';
          public          odoo    false    315                       0    0    COLUMN account_move.ref    COMMENT     :   COMMENT ON COLUMN public.account_move.ref IS 'Reference';
          public          odoo    false    315                       0    0    COLUMN account_move.date    COMMENT     6   COMMENT ON COLUMN public.account_move.date IS 'Date';
          public          odoo    false    315                       0    0    COLUMN account_move.journal_id    COMMENT     ?   COMMENT ON COLUMN public.account_move.journal_id IS 'Journal';
          public          odoo    false    315                       0    0    COLUMN account_move.currency_id    COMMENT     A   COMMENT ON COLUMN public.account_move.currency_id IS 'Currency';
          public          odoo    false    315                       0    0    COLUMN account_move.state    COMMENT     9   COMMENT ON COLUMN public.account_move.state IS 'Status';
          public          odoo    false    315                       0    0    COLUMN account_move.partner_id    COMMENT     ?   COMMENT ON COLUMN public.account_move.partner_id IS 'Partner';
          public          odoo    false    315                       0    0    COLUMN account_move.amount    COMMENT     :   COMMENT ON COLUMN public.account_move.amount IS 'Amount';
          public          odoo    false    315                       0    0    COLUMN account_move.narration    COMMENT     D   COMMENT ON COLUMN public.account_move.narration IS 'Internal Note';
          public          odoo    false    315                       0    0    COLUMN account_move.company_id    COMMENT     ?   COMMENT ON COLUMN public.account_move.company_id IS 'Company';
          public          odoo    false    315                       0    0 &   COLUMN account_move.matched_percentage    COMMENT     R   COMMENT ON COLUMN public.account_move.matched_percentage IS 'Percentage Matched';
          public          odoo    false    315                       0    0 )   COLUMN account_move.tax_cash_basis_rec_id    COMMENT     Z   COMMENT ON COLUMN public.account_move.tax_cash_basis_rec_id IS 'Tax Cash Basis Entry of';
          public          odoo    false    315                       0    0     COLUMN account_move.auto_reverse    COMMENT     O   COMMENT ON COLUMN public.account_move.auto_reverse IS 'Reverse Automatically';
          public          odoo    false    315                       0    0     COLUMN account_move.reverse_date    COMMENT     G   COMMENT ON COLUMN public.account_move.reverse_date IS 'Reversal Date';
          public          odoo    false    315                       0    0 $   COLUMN account_move.reverse_entry_id    COMMENT     K   COMMENT ON COLUMN public.account_move.reverse_entry_id IS 'Reverse Entry';
          public          odoo    false    315                       0    0    COLUMN account_move.create_uid    COMMENT     B   COMMENT ON COLUMN public.account_move.create_uid IS 'Created by';
          public          odoo    false    315                       0    0    COLUMN account_move.create_date    COMMENT     C   COMMENT ON COLUMN public.account_move.create_date IS 'Created on';
          public          odoo    false    315                       0    0    COLUMN account_move.write_uid    COMMENT     F   COMMENT ON COLUMN public.account_move.write_uid IS 'Last Updated by';
          public          odoo    false    315                       0    0    COLUMN account_move.write_date    COMMENT     G   COMMENT ON COLUMN public.account_move.write_date IS 'Last Updated on';
          public          odoo    false    315                       0    0 !   COLUMN account_move.stock_move_id    COMMENT     E   COMMENT ON COLUMN public.account_move.stock_move_id IS 'Stock Move';
          public          odoo    false    315            <           1259    1110878    account_move_id_seq    SEQUENCE        CREATE SEQUENCE public.account_move_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.account_move_id_seq;
       public          odoo    false    315                       0    0    account_move_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.account_move_id_seq OWNED BY public.account_move.id;
          public          odoo    false    316            η           2604    1123392    account_move id    DEFAULT     r   ALTER TABLE ONLY public.account_move ALTER COLUMN id SET DEFAULT nextval('public.account_move_id_seq'::regclass);
 >   ALTER TABLE public.account_move ALTER COLUMN id DROP DEFAULT;
       public          odoo    false    316    315            u          0    1110872    account_move 
   TABLE DATA             COPY public.account_move (id, name, ref, date, journal_id, currency_id, state, partner_id, amount, narration, company_id, matched_percentage, tax_cash_basis_rec_id, auto_reverse, reverse_date, reverse_entry_id, create_uid, create_date, write_uid, write_date, stock_move_id) FROM stdin;
    public          odoo    false    315   	0                  0    0    account_move_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.account_move_id_seq', 1, false);
          public          odoo    false    316            κ           2606    1113916    account_move account_move_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.account_move
    ADD CONSTRAINT account_move_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.account_move DROP CONSTRAINT account_move_pkey;
       public            odoo    false    315            θ           1259    1114821    account_move_date_index    INDEX     P   CREATE INDEX account_move_date_index ON public.account_move USING btree (date);
 +   DROP INDEX public.account_move_date_index;
       public            odoo    false    315            λ           2606    1116625 )   account_move account_move_company_id_fkey    FK CONSTRAINT     €   ALTER TABLE ONLY public.account_move
    ADD CONSTRAINT account_move_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.res_company(id) ON DELETE SET NULL;
 S   ALTER TABLE ONLY public.account_move DROP CONSTRAINT account_move_company_id_fkey;
       public          odoo    false    315            μ           2606    1116630 )   account_move account_move_create_uid_fkey    FK CONSTRAINT     ’   ALTER TABLE ONLY public.account_move
    ADD CONSTRAINT account_move_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES public.res_users(id) ON DELETE SET NULL;
 S   ALTER TABLE ONLY public.account_move DROP CONSTRAINT account_move_create_uid_fkey;
       public          odoo    false    315            ν           2606    1116635 *   account_move account_move_currency_id_fkey    FK CONSTRAINT     §   ALTER TABLE ONLY public.account_move
    ADD CONSTRAINT account_move_currency_id_fkey FOREIGN KEY (currency_id) REFERENCES public.res_currency(id) ON DELETE SET NULL;
 T   ALTER TABLE ONLY public.account_move DROP CONSTRAINT account_move_currency_id_fkey;
       public          odoo    false    315            ξ           2606    1116640 )   account_move account_move_journal_id_fkey    FK CONSTRAINT     ¨   ALTER TABLE ONLY public.account_move
    ADD CONSTRAINT account_move_journal_id_fkey FOREIGN KEY (journal_id) REFERENCES public.account_journal(id) ON DELETE SET NULL;
 S   ALTER TABLE ONLY public.account_move DROP CONSTRAINT account_move_journal_id_fkey;
       public          odoo    false    315            ο           2606    1116750 )   account_move account_move_partner_id_fkey    FK CONSTRAINT     €   ALTER TABLE ONLY public.account_move
    ADD CONSTRAINT account_move_partner_id_fkey FOREIGN KEY (partner_id) REFERENCES public.res_partner(id) ON DELETE SET NULL;
 S   ALTER TABLE ONLY public.account_move DROP CONSTRAINT account_move_partner_id_fkey;
       public          odoo    false    315            π           2606    1116770 /   account_move account_move_reverse_entry_id_fkey    FK CONSTRAINT     ±   ALTER TABLE ONLY public.account_move
    ADD CONSTRAINT account_move_reverse_entry_id_fkey FOREIGN KEY (reverse_entry_id) REFERENCES public.account_move(id) ON DELETE SET NULL;
 Y   ALTER TABLE ONLY public.account_move DROP CONSTRAINT account_move_reverse_entry_id_fkey;
       public          odoo    false    315    5098    315            ρ           2606    1116775 ,   account_move account_move_stock_move_id_fkey    FK CONSTRAINT     ©   ALTER TABLE ONLY public.account_move
    ADD CONSTRAINT account_move_stock_move_id_fkey FOREIGN KEY (stock_move_id) REFERENCES public.stock_move(id) ON DELETE SET NULL;
 V   ALTER TABLE ONLY public.account_move DROP CONSTRAINT account_move_stock_move_id_fkey;
       public          odoo    false    315            ς           2606    1116780 4   account_move account_move_tax_cash_basis_rec_id_fkey    FK CONSTRAINT     Θ   ALTER TABLE ONLY public.account_move
    ADD CONSTRAINT account_move_tax_cash_basis_rec_id_fkey FOREIGN KEY (tax_cash_basis_rec_id) REFERENCES public.account_partial_reconcile(id) ON DELETE SET NULL;
 ^   ALTER TABLE ONLY public.account_move DROP CONSTRAINT account_move_tax_cash_basis_rec_id_fkey;
       public          odoo    false    315            σ           2606    1116785 (   account_move account_move_write_uid_fkey    FK CONSTRAINT         ALTER TABLE ONLY public.account_move
    ADD CONSTRAINT account_move_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES public.res_users(id) ON DELETE SET NULL;
 R   ALTER TABLE ONLY public.account_move DROP CONSTRAINT account_move_write_uid_fkey;
       public          odoo    false    315            u      xΡγββ Ε ©     