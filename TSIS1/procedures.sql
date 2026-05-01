-- Телефон қосу процедурасы
CREATE OR REPLACE PROCEDURE add_phone(p_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE v_id INT;
BEGIN
    SELECT id INTO v_id FROM contacts WHERE first_name = p_name OR last_name = p_name LIMIT 1;
    IF v_id IS NOT NULL THEN
        INSERT INTO phones (contact_id, phone, type) VALUES (v_id, p_phone, p_type);
    END IF;
END; $$;

-- Топқа ауыстыру процедурасы
CREATE OR REPLACE PROCEDURE move_to_group(p_name VARCHAR, p_group VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE v_g_id INT;
BEGIN
    INSERT INTO groups (name) VALUES (p_group) ON CONFLICT (name) DO NOTHING;
    SELECT id INTO v_g_id FROM groups WHERE name = p_group;
    UPDATE contacts SET group_id = v_g_id WHERE first_name = p_name OR last_name = p_name;
END; $$;

-- Күрделі іздеу функциясы (Пункт 10 үшін)
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(id INT, first_name VARCHAR, last_name VARCHAR, email VARCHAR, birthday DATE, group_name VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT c.id, c.first_name, c.last_name, c.email, c.birthday, g.name
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE c.first_name ILIKE '%' || p_query || '%' 
       OR c.last_name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%' 
       OR p.phone ILIKE '%' || p_query || '%';
END; $$ LANGUAGE plpgsql;

-- Пагинация функциясы (Пункт 4 үшін)
DROP FUNCTION IF EXISTS get_contacts_paginated(INT, INT);

CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(id INT, first_name VARCHAR, last_name VARCHAR, email VARCHAR, birthday DATE, group_name VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.first_name, c.last_name, c.email, c.birthday, g.name
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    ORDER BY c.first_name
    LIMIT p_limit OFFSET p_offset;
END; $$ LANGUAGE plpgsql;